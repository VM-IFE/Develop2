from odoo import models, api
from psycopg2 import sql
from odoo.addons.account_reports.models.account_analytic_report import AccountReport as AccountReportOrigin


@api.model
def _prepare_lines_for_analytic_groupby(self):
    """Prepare the analytic_temp_account_move_line

    This method should be used once before all the SQL queries using the
    table account_move_line for the analytic columns for the financial reports.
    It will create a new table with the schema of account_move_line table, but with
    the data from account_analytic_line.

    We inherit the schema of account_move_line, make the correspondence between
    account_move_line fields and account_analytic_line fields and put NULL for those
    who don't exist in account_analytic_line.
    We also drop the NOT NULL constraints for fields who are not required in account_analytic_line.
    """
    self.env.cr.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name='analytic_temp_account_move_line'")
    if self.env.cr.fetchone():
        return

    line_fields = self.env['account.move.line'].fields_get()
    self.env.cr.execute("SELECT column_name FROM information_schema.columns WHERE table_name='account_move_line'")
    stored_fields = set(f[0] for f in self.env.cr.fetchall())
    changed_equivalence_dict = {
        "id": sql.Identifier("id"),
        "balance": sql.SQL("-amount"),
        "company_id": sql.Identifier("company_id"),
        "journal_id": sql.Identifier("journal_id"),
        "display_type": sql.Literal("product"),
        "parent_state": sql.Literal("posted"),
        "date": sql.Identifier("date"),
        "account_id": sql.Identifier("general_account_id"),
        "partner_id": sql.Identifier("partner_id"),
        "debit": sql.SQL("CASE WHEN (amount < 0) THEN amount else 0 END"),
        "credit": sql.SQL("CASE WHEN (amount > 0) THEN amount else 0 END"),
    }
    selected_fields = []
    for fname in stored_fields:
        if fname in changed_equivalence_dict:
            selected_fields.append(sql.SQL('{original} AS "account_move_line.{asname}"').format(
                original=changed_equivalence_dict[fname],
                asname=sql.SQL(fname),
            ))
        elif fname == 'analytic_distribution':
            selected_fields.append(sql.SQL('to_jsonb(account_id) AS "account_move_line.analytic_distribution"'))
        else:
            if line_fields[fname].get("type") in ("many2one", "one2many", "many2many", "monetary"):
                typecast = sql.SQL('integer')
            elif line_fields[fname].get("type") == "datetime":
                typecast = sql.SQL('date')
            elif line_fields[fname].get("type") in ("selection", "html"):
                typecast = sql.SQL('text')
            else:
                typecast = sql.SQL(line_fields[fname].get("type"))
            selected_fields.append(sql.SQL('cast(NULL AS {typecast}) AS "account_move_line.{fname}"').format(
                typecast=typecast,
                fname=sql.SQL(fname),
            ))

    query = sql.SQL("""
        -- Create a temporary table, dropping not null constraints because we're not filling those columns
        CREATE TEMPORARY TABLE IF NOT EXISTS analytic_temp_account_move_line () inherits (account_move_line) ON COMMIT DROP;
        ALTER TABLE analytic_temp_account_move_line NO INHERIT account_move_line;
        ALTER TABLE analytic_temp_account_move_line ALTER COLUMN move_id DROP NOT NULL;
        ALTER TABLE analytic_temp_account_move_line ALTER COLUMN currency_id DROP NOT NULL;

        INSERT INTO analytic_temp_account_move_line ({all_fields})
        SELECT {table}
        FROM (SELECT * FROM account_analytic_line WHERE general_account_id IS NOT NULL) AS account_analytic_line
    """).format(
        all_fields=sql.SQL(', ').join(sql.Identifier(fname) for fname in stored_fields),
        table=sql.SQL(', ').join(selected_fields),
    )

    # TODO gawa need to do the auditing of the lines
    # TODO gawa try to reduce query on analytic lines

    self.env.cr.execute(query)

AccountReportOrigin._prepare_lines_for_analytic_groupby = _prepare_lines_for_analytic_groupby