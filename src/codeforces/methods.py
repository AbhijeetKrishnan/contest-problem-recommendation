import hashlib
import secrets
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from pydantic import BaseModel
from requests.exceptions import ConnectionError, HTTPError, Timeout

from .objects import (
    BlogEntry,
    Comment,
    Contest,
    Hack,
    Problem,
    ProblemStatistics,
    RanklistRow,
    RatingChange,
    RecentAction,
    Submission,
    User,
)

DEFAULT_TIMEOUT = 9.01
CF_API = "https://codeforces.com/api"


def getCfAuth(
    key: int, secret: int, methodName: str, payload: Dict[str, Any]
) -> Dict[str, Any]:
    "Add required fields to the payload as per Codeforces authentication requirements"

    apiKey = key
    currTime = int(time.time())
    payload["apiKey"] = apiKey
    payload["time"] = currTime

    rand = secrets.token_urlsafe(6)[:6]
    sortedParams = "&".join(
        [f"{param}={value}" for param, value in sorted(payload.items())]
    )
    randStr = f"{rand}/{methodName}?{sortedParams}#{secret}"
    hash = hashlib.sha512(randStr.encode("utf-8"))
    payload["apiSig"] = f"{rand}{hash}"
    return payload


def getBlogEntryComments(blogEntryId: int) -> Optional[List[Comment]]:
    "Returns a list of comments to the specified blog entry."

    methodName = "blogEntry.comments"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {"blogEntryId": blogEntryId}
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [Comment.parse_obj(comment) for comment in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getBlogEntryView(blogEntryId: int) -> Optional[BlogEntry]:
    "Returns blog entry."

    methodName = "blogEntry.view"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {"blogEntryId": blogEntryId}
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return BlogEntry.parse_obj(result)
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getContestHacks(contestId: int, asManager: Optional[bool]) -> Optional[List[Hack]]:
    "Returns list of hacks in the specified contests. Full information about hacks is available only after some time after the contest end. During the contest user can see only own hacks."

    methodName = "contest.hacks"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {"contestId": contestId, "asManager": asManager}
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [Hack.parse_obj(hack) for hack in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getContestList(gym: Optional[bool]) -> Optional[List[Contest]]:
    "Returns information about all available contests."

    methodName = "contest.list"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {"gym": gym}
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [Contest.parse_obj(contest) for contest in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getContestRatingChanges(contestId: int) -> Optional[List[RatingChange]]:
    "Returns rating changes after the contest."

    methodName = "contest.ratingChanges"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "contestId": contestId,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [RatingChange.parse_obj(rc) for rc in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


class ContestStandings(BaseModel):
    contest: Contest
    problems: List[Problem]
    rows: List[RanklistRow]


def getContestStandings(
    contestId: int,
    asManager: Optional[bool] = None,
    from_: Optional[int] = None,
    count: Optional[int] = None,
    handles: Optional[List[str]] = None,
    room: Optional[int] = None,
    showUnofficial: Optional[bool] = None,
) -> Optional[ContestStandings]:
    "Returns the description of the contest and the requested part of the standings."

    methodName = "contest.standings"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "contestId": contestId,
        "asManager": asManager,
        "from": from_,
        "count": count,
        "handles": ";".join(handles) if handles else handles,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return ContestStandings.parse_obj(result)
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getContestStatus(
    contestId: int,
    handle: str,
    from_: Optional[int] = None,
    count: Optional[int] = None,
    asManager: Optional[bool] = None,
) -> Optional[List[Submission]]:
    "Returns submissions for specified contest. Optionally can return submissions of specified user."

    methodName = "contest.status"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "contestId": contestId,
        "asManager": asManager,
        "handle": handle,
        "from": from_,
        "count": count,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [Submission.parse_obj(submission) for submission in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getProblemsetProblems(
    tags: List[str], problemsetName: Optional[str] = None
) -> Optional[Tuple[List[Problem], List[ProblemStatistics]]]:
    "Returns all problems from problemset. Problems can be filtered by tags."

    methodName = "problemset.problems"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "tags": ";".join(tags),
        "problemsetName": problemsetName,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            problems, problemStatistics = result
            return [Problem.parse_obj(problem) for problem in problems], [
                ProblemStatistics.parse_obj(probStat) for probStat in problemStatistics
            ]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getProblemsetRecentStatus(
    count: int, problemsetName: Optional[str]
) -> Optional[List[Submission]]:
    "Returns recent submissions."

    methodName = "problemset.recentStatus"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "count": count,
        "problemsetName": problemsetName,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [Submission.parse_obj(sub) for sub in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getRecentActions(maxCount: int) -> Optional[List[RecentAction]]:
    "Returns recent actions."

    methodName = "recentActions"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "maxCount": maxCount,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [RecentAction.parse_obj(recentAction) for recentAction in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getUserBlogEntries(handle: str) -> Optional[List[BlogEntry]]:
    "Returns a list of all user's blog entries."

    methodName = "user.blogEntries"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "handle": handle,
    }
    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [BlogEntry.parse_obj(blogEntry) for blogEntry in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getUserFriends(
    key: int, secret: int, onlyOnline: Optional[bool] = None
) -> Optional[List[str]]:
    "Returns authorized user's friends. Using this method requires authorization."

    methodName = "user.friends"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "onlyOnline": onlyOnline,
    }
    payload = getCfAuth(key, secret, methodName, payload)

    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return result
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getUserInfo(handles: List[str]) -> Optional[List[User]]:
    "Returns information about one or several users."

    methodName = "user.info"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "handles": ";".join(handles),
    }

    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [User.parse_obj(user) for user in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getUserRatedList(
    activeOnly: Optional[bool] = None,
    includeRetired: Optional[bool] = None,
    contestId: Optional[int] = None,
) -> Optional[List[User]]:
    "Returns the list users who have participated in at least one rated contest."

    methodName = "user.ratedList"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "activeOnly": activeOnly,
        "includeRetired": includeRetired,
        "contestId": contestId,
    }

    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [User.parse_obj(user) for user in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getUserRating(handle: str) -> Optional[List[RatingChange]]:
    "Returns rating history of the specified user."

    methodName = "user.rating"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "handle": handle,
    }

    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [RatingChange.parse_obj(rc) for rc in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def getUserStatus(
    handle: str, from_: Optional[int], count: Optional[int]
) -> Optional[List[Submission]]:
    "Returns submissions of specified user."

    methodName = "user.status"
    url = f"{CF_API}/{methodName}"
    timeout = DEFAULT_TIMEOUT
    payload = {
        "handle": handle,
    }

    try:
        r = requests.get(url, payload, timeout=timeout)
        if r.status_code == 200:
            result = r.json()["result"]
            return [Submission.parse_obj(sub) for sub in result]
    except Timeout:
        print(f"Timeout on request to {methodName} after {timeout} seconds.")
    except ConnectionError:
        print(f"Connection error on request to {methodName}.")
    except HTTPError as err:
        print(
            f"Unsuccessful response code {err} on request to {methodName}. Response recieved is {r.json()}"
        )
    return None


def main():
    standings = getContestStandings(566, from_=1, count=5)
    print(standings)


if __name__ == "__main__":
    main()
