from typing import Any, Dict, List, Optional, Tuple, Type, TypedDict

import requests
from objects import (
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
from pydantic import BaseModel, create_model
from requests.exceptions import ConnectionError, HTTPError, Timeout

DEFAULT_TIMEOUT = 9.01
CF_API = "https://codeforces.com/api"


class ApiMethod:
    def __init__(
        self,
        methodName: str,
        payloadSchema: Dict[str, Any],
        returnSchema: Tuple[Type, Any],
        baseUrl: str = CF_API,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self._methodName = methodName
        self._url = f"{baseUrl}/{methodName}"
        self._payloadModel = create_model(methodName, **payloadSchema)
        self._returnModel = create_model(
            f"return_{methodName}", status=str, result=returnSchema
        )
        self._timeout = timeout

    def makeRequest(self, payload: Dict[str, Any]) -> Optional[BaseModel]:
        try:
            _ = self._payloadModel(**payload)
            r = requests.get(self._url, payload, timeout=self._timeout)
            if r.status_code == 200:
                returnValue = self._returnModel(**r.json())
                return returnValue.result
            else:
                r.raise_for_status()
        except ValueError as v:
            print(f"Invalid payload {payload} to {self._methodName}: {v}")
        except Timeout:
            print(
                f"Timeout on request to {self._methodName} after {self._timeout} seconds."
            )
        except ConnectionError:
            print(f"Connection error on request to {self._methodName}.")
        except HTTPError as err:
            print(
                f"Unsuccessful response code {err} on request to {self._methodName}. Response recieved is {r.json()}"
            )
        return None


class ContestStandings(BaseModel):
    contest: Contest
    problems: List[Problem]
    rows: List[RanklistRow]


# TODO: what's the most ergonomic way to set this up?
CF_API_METHODS = {
    "getBlogEntryComments": ApiMethod(
        "blogEntry.comments", {"blogEntryId": (int, ...)}, (List[Comment], ...)
    ),
    "getBlogEntryView": ApiMethod(
        "blogEntry.view", {"blogEntryId": (int, ...)}, (BlogEntry, ...)
    ),
    "getContestHacks": ApiMethod(
        "contest.hacks",
        {"contestId": (int, ...), "asManager": (bool, None)},
        (List[Hack], ...),
    ),
    "getContestList": ApiMethod(
        "contest.list", {"gym": (bool, None)}, (List[Contest], ...)
    ),
    "getContestRatingChanges": ApiMethod(
        "contest.ratingChanges", {"contestId": (int, ...)}, (List[RatingChange], ...)
    ),
    "getContestStandings": ApiMethod(
        "contest.standings",
        {
            "contestId": (int, ...),
            "asManager": (bool, None),
            "from": (int, None),
            "count": (int, None),
            "handles": (str, None),
            "room": (int, None),
            "showUnofficial": (bool, None),
        },
        (ContestStandings, ...),
    ),
}


def getContestStatus(
    contestId: int, handle: str, from_: int, count: int, asManager: bool = False
) -> List[Submission]:
    pass


def getProblemsetProblems(
    tags: List[str], problemsetName: str
) -> Tuple[List[Problem], List[ProblemStatistics]]:
    pass


def getProblemsetRecentStatus(count: int, problemsetName: str) -> List[Submission]:
    pass


def getRecentActions(maxCount: int) -> List[RecentAction]:
    pass


def getUserBlogEntries(handle: str) -> List[BlogEntry]:
    pass


def getUserFriends(onlyOnline: bool) -> List[str]:
    pass


def getUserInfo(handles: List[str]) -> List[User]:
    pass


def getUserRatedList(
    activeOnly: bool, includeRetired: bool, contestId: int
) -> List[User]:
    pass


def getUserRating(handle: str) -> List[RatingChange]:
    pass


def getUserStatus(handle: str, from_: int, count: int) -> List[Submission]:
    pass


def main():
    standings = CF_API_METHODS["getContestStandings"].makeRequest(
        {"contestId": 566, "from": 1, "count": 5}
    )
    print(standings)
    import code

    code.interact(local=locals())


if __name__ == "__main__":
    main()
