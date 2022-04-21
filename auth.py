# INSTALLATION:
# pip install fyers-apiv2

# AUTHORIZATION:
from tqdm import tqdm
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import pandas as pd
from conf import client_id,redirect_url,secret_key


session=accessToken.SessionModel(client_id=client_id,
secret_key=secret_key,redirect_uri=redirect_url, 
response_type='code',grant_type='authorization_code')

response = session.generate_authcode() 
print(response)
print('*'*100)
auth_code = input("enter auth code")
print('*'*100)
print(auth_code)
print('*'*100)


session.set_token(auth_code)
print(f'Session created: {session}')


response = session.generate_token()

print('Response: ',response)
access_token = response['access_token']

# print(f'{access_token}')

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,log_path=r"C:\Users\apurv\Desktop\fyers")


print('*'*100)
print(fyers.get_profile())

print('*'*100)
print('*'*100)

def make_time(ts):
    ts = int(ts)
    date = datetime.datetime.utcfromtimestamp(ts) + datetime.timedelta(minutes=30, hours=5)
    return date

def find_range(candles):
    c = candles['candles']
    return make_time(c[0][0]), make_time(c[-1][0])

end_date = datetime.datetime.now().date()
start_date = end_date - datetime.timedelta(days=98)
c = []
for i in tqdm(range(100)):
    try:
        print(f'From Range {start_date} - {end_date}')
        data = {"symbol":"NSE:SBIN-EQ",
                "resolution":"1",
                "date_format":"1",
                "range_from":str(start_date),
                "range_to":str(end_date),
                "cont_flag":"1"}
        candles = fyers.history(data)

        print(candles['s'])
        print(len(candles['candles']))
        print(find_range(candles))
        
        end_date = start_date - - datetime.timedelta(days=1)
        start_date = start_date - datetime.timedelta(days=98)
        c = c + candles['candles']
        print('*'*100)
    except Exception as e:
        print(f"Error encountered {e}")
        print(candles['candles'])
        break
print('saving data...')
df = pd.DataFrame(c,columns=['Date','Open','High','Low','Close','Volume'])
df.Date = df.Date.apply(make_time)
df.set_index('Date',inplace=True)
df.to_csv('SBIN.csv')
print('saved data...')