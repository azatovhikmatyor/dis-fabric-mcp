from app.utils.sql_loader import load_sql


def test_load_sql():
    sql = load_sql("product/find_product_code.sql")
    assert "SELECT" in sql
