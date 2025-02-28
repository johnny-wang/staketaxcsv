
from osmo.make_tx import make_osmo_unknown_tx, make_osmo_unknown_tx_with_transfer


def handle_unknown_detect_transfers(exporter, txinfo, msginfo):
    transfers_in, transfers_out = msginfo.transfers

    if len(transfers_in) == 0 and len(transfers_out) == 0:
        handle_unknown(exporter, txinfo, msginfo)
        return
    elif len(transfers_in) == 1 and len(transfers_out) == 1:
        # Present unknown transaction as one line (for this special case).
        sent_amount, sent_currency = transfers_out[0]
        received_amount, received_currency = transfers_in[0]

        row = make_osmo_unknown_tx_with_transfer(
            txinfo, msginfo, sent_amount, sent_currency, received_amount, received_currency)
        exporter.ingest_row(row)
    else:
        # Present unknown transaction as separate transfers.
        i = 0
        for sent_amount, sent_currency in transfers_out:
            row = make_osmo_unknown_tx_with_transfer(
                txinfo, msginfo, sent_amount, sent_currency, "", "", empty_fee=(i > 0), z_index=i
            )
            exporter.ingest_row(row)
            i += 1
        for received_amount, received_currency in transfers_in:
            row = make_osmo_unknown_tx_with_transfer(
                txinfo, msginfo, "", "", received_amount, received_currency, empty_fee=(i > 0), z_index=i
            )
            exporter.ingest_row(row)
            i += 1


def handle_unknown(exporter, txinfo, msginfo):
    row = make_osmo_unknown_tx(txinfo, msginfo)
    exporter.ingest_row(row)
