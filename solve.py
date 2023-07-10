import json
import requests
from image_detector import solve_image


def get_solutions(cs):
    return requests.post("http://127.0.0.1:8000/solve", json={
        "challenges": cs
    }).json()['solutions']


captcha_token = "EuNN2AjxcxgpKAxKCrcgIqwb" # not sure what this is for. seems to be static but maybe it changes from time to time. at the time of uploading this, its working perfectly fine with this set.

first_request = requests.get(f"https://account-api.proton.me/captcha/v1/api/init?challengeType=2D&parentURL=https://account-api.proton.me/core/v4/captcha?Token={captcha_token}&ForceWebMessaging=1&displayedLang=en&supportedLangs=en-US,en-US,en,en-US,en&purpose=signup")

img = requests.get("https://account-api.proton.me/captcha/v1/api/bg", params={
    "token": first_request.json()['token']
})

t = solve_image(img.content)
if t is None:
    exit()

challenges = first_request.json()['challenges']
answers = get_solutions(challenges)

print(t, answers)

captcha_object = {
    "x": t[0],
    "y": t[1],
    "answers": answers,
    "clientData": None,
    "pieceLoadElapsedMs": 140,
    "bgLoadElapsedMs": 180,
    "challengeLoadElapsedMs": 180,
    "solveChallengeMs": 5000,
    "powElapsedMs": 540
}

submit_request = requests.get("https://account-api.proton.me/captcha/v1/api/validate", params={
    "token": first_request.json()['token'],
    "contestId": first_request.json()['contestId'],
    "purpose": "signup"
}, headers={
    "pcaptcha": json.dumps(captcha_object)
})

print(submit_request.text)
