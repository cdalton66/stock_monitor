def test_import():
    import stock_monitor
    assert hasattr(stock_monitor, 'STOCKS')
