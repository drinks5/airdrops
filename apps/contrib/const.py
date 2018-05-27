# encoding: utf-8
import socks
import os

Proxy = (socks.SOCKS5, '127.0.0.1', 1080)
InjectedChats = 'InjectedChats'  # 需要被拦截的会话
Telegram = 'Telegram'
TelegramPhone = '42277'
Tcp = ('0.0.0.0', 9999)
MaxBuffer = 1024 * 512


class Cache:
    account = 'account'


RecaptchaCookie = {
    'SID':
    'IwYeV0k04fyAgWrWaIDqIXPKb-9VamgLS4GJJPl8pyAzQgcVKzBZEPINDHLpS_UasP_Dww.',
    'HSID':
    'ANfbfgRdQOAETeubh',
    'SSID':
    'Auzpcj3IgnhArjAKQ',
    'APISID':
    '6GX8BUW0fPGhX1sM/An_lCeCsOFzyV1-Wl',
    'SAPISID':
    'uO-eSrQSf4WXaD4t/AIwX4oRKNQ8SAzTJp',
    'SIDCC':
    'AEfoLeYMctivGoDtI4qJYHKtjinEy1X9Cytu3EPDeOVbsu36PxwyO4EdZQ9d02G1h7nWhhpEVqU',
    'NID':
    '130=axlNpGL_ULPG19VBUoMudkw7zVAqB8mHyb5DhdsfJ1uun3Rlok-Xsj8XvkXZWhThfgWbAXQGNsGRrOTuWesuti20_amJcRK-pKpHyLBobLPjxE5EXSVhKr9vF-EM5mNOdZO_ngJ9OXh8joPvSTtfBl7XeFWUpXfKz8VC7q6CjypvlHlAkl-44LBzoWQOUSF7IHmIGO82hiiwTpfgiCRZ4GF1M_N_hZvFl8gnPp3VNX8M'
    # 'UULE': 'a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTUyNjgxOTQ2MjI1NTAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MzEzMDQxNzA0IGxvbmdpdHVkZV9lNzoxMjE0MDUyMDk2fSByYWRpdXM6MjY2NjA=',
    # '1P_JAR': '2018-05-20-12',  #
    # 'S': 'billing-ui-v3=REOKK54kC1ycjjPaFWWs7uaUwhgfdGNO:billing-ui-v3-efe=REOKK54kC1ycjjPaFWWs7uaUwhgfdGNO'
}
"""
https://www.ishopforipsos.com/en_GB/page/detail/cookies
https://www.publicdesire.com/cookies
1P_JAR: These cookies are used to gather website statistics, and track conversion rates.
NID: The NID cookie contains a unique ID Google uses to remember your preferences and other information, such as your preferred language (e.g. English), how many search results you wish to have shown per page (e.g. 10 or 20), and whether or not you wish to have Google’s SafeSearch filter turned on.
SID: Contains encrypted records of a user’s account ID and most recent sign-in time as well as his country and language preferences.

NID
SNID
SIDCC   Google tracking cookies
"""
