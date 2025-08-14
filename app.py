from flask import Flask, request, jsonify, render_template, redirect, make_response
from pyquotex.stable_api import Quotex
import traceback, json, os, random, threading, time, requests as rq, logging

# for logger_name in logging.root.manager.loggerDict:
#     if not logger_name.startswith("waitress"):
#         logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# os.environ['RES_PATH'] = '/tmp'
PROXIES = [
    # 'socks5h://mariam:mariam_1@27.131.14.77:9169',
    # 'socks5h://mariam1:mariam_1@103.134.60.86:9169'
]

print('Fetching Base HTTP Url for Quotex', flush=True)
while 1:
    try:
        rxp = random.choice(PROXIES or [None])
        os.environ['QX_HTTPS_BASE'] = '/'.join(rq.get('https://qxbroker.com', verify=False, proxies=dict(http=rxp, https=rxp) if rxp else None).url.split('/', 3)[:3])
        break
    except rq.exceptions.ConnectionError: pass
print('Done', flush=True)

app = Flask(__name__)
client = Quotex("drive4341@gmail.com", "drive@1", "en")
has_connect_run = False

@app.before_request
def set_suffled_proxy():
    if not request.args.get('market'): return
    prev_pr = os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')
    if prev_pr: return
    uniq_pr = [p for p in PROXIES if p != prev_pr]
    pr = random.choice(uniq_pr or PROXIES or [None])
    if pr:
        os.environ['HTTP_PROXY'] = pr
        os.environ['HTTPS_PROXY'] = pr


@app.after_request
def remove_proxy(res):
    if not request.args.get('market'): return res
    try:
        del os.environ['HTTP_PROXY']
        del os.environ['HTTPS_PROXY']
    except KeyError: pass
    except:
        traceback.print_exc()
    return res


@app.route('/')
async def index():
    print('reqqqqqq')
    global has_connect_run
    market = request.args.get('market')
    period = request.args.get('period', 60, int)
    isJson = 'application/json' in request.headers.get('Accept', '')
    
    if not market:
        return """
        <html>
            <head>
                <title>Quotex API</title>
            </head>
            <body>
            <h2>Missing required argument: <code>market</code></h2>
            <p>
                <b>Arguments:</b>
                <ul>
                <li><b>market</b> <span style="color:red;">(required)</span>: The market symbol to fetch candles for (e.g., <code>EURUSD</code> <code>EURUSD_otc</code>).</li>
                <li><b>period</b> (optional): Candle period in seconds. Default: <code>60</code></li>
                </ul>
            </p>
            <b>Send <code>Accept: application/json</code> header to get json response</b>
            </body>
        </html>
        """

    try:
        if not has_connect_run:
            success, message = await client.connect()
            if not success:
                if 'Handshake status 525'.lower() in str(message).lower(): return redirect(request.full_path)
                if 'Handshake status 403 Forbidden'.lower() in str(message).lower():
                    return redirect(request.full_path)
                if isJson: return jsonify(dict(success=False, msg=f'Cannot Login. Make sure that 2fa is off. Message: {message}'))
                else: return f'<h3>Cannot Login. Make sure that 2fa is off. Message: {message}</h3>'
            has_connect_run = True
        candles = await client.get_candle_v2(market, period)
        if isJson: return jsonify(dict(success=True, candles=candles))
        return render_template('chart.html', candles_str=json.dumps(candles), market=market)
    except Exception as err:
        if 'socket is already closed' in str(err): return redirect(request.full_path)
        traceback.print_exc()
        if isJson: return make_response(jsonify(dict(success=False, msg=f'Internal Server Error. {err}')), 500)
        else: return make_response(f'<h1>Internal Server Error</h1><br/><pre><code>{err}</code></pre>', 500)


def pingSelf():
    while 1:
        try:
            rq.get('http://127.0.0.1:8000/?market=EURUSD')
            print('Keep Connection', flush=True)
        except rq.exceptions.ConnectionError: continue
        except:
            traceback.print_exc()
        time.sleep(3 * 60)

threading.Thread(target=pingSelf, daemon=True).start()

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)
