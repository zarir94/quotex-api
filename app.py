from flask import Flask, request, jsonify, render_template, redirect
from pyquotex.stable_api import Quotex
import traceback, json, os
# os.environ['RES_PATH'] = '/tmp'

app = Flask(__name__)

@app.route('/')
async def index():
    email = request.args.get('email', "drive4341@gmail.com")
    password = request.args.get('password', "drive@1")
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
                <li><b>email</b> (optional): Your Quotex account email.</li>
                <li><b>password</b> (optional): Your Quotex account password.</li>
                <li><b>market</b> <span style="color:red;">(required)</span>: The market symbol to fetch candles for (e.g., <code>EURUSD</code> <code>EURUSD_otc</code>).</li>
                <li><b>period</b> (optional): Candle period in seconds. Default: <code>60</code></li>
                </ul>
            </p>
            <b>Send <code>Accept: application/json</code> header to get json response</b>
            </body>
        </html>
        """

    try:
        client = Quotex(email, password, "en")
        success, message = await client.connect()
        if not success:
            if 'Handshake status 403 Forbidden'.lower() in str(message).lower():
                return redirect(request.full_path)
            if isJson: return jsonify(dict(success=False, msg=f'Cannot Login. Make sure that 2fa is off. Message: {message}'))
            else: return f'<h3>Cannot Login. Make sure that 2fa is off. Message: {message}</h3>'
        candles = await client.get_candle_v2(market, period)
        await client.close()
        if isJson: return jsonify(dict(success=True, candles=candles))
        return render_template('chart.html', candles_str=json.dumps(candles), market=market)
    except Exception as err:
        return str(err)
        traceback.print_exc()
        if isJson: return jsonify(dict(success=False, msg=f'Internal Server Error. {err}'))
        else: return f'<h1>Internal Server Error</h1><br/><pre><code>{err}</code></pre>'


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)
