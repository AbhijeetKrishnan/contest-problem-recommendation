from typing import List, Tuple, TypedDict

import requests

from .objects import (BlogEntry, Comment, Contest, Hack, Problem,
                      ProblemStatistics, RanklistRow, RatingChange,
                      RecentAction, Submission, User)

# TODO: better way to use the requests library to pass args rather than forming
# a string template?
CF_API = 'https://codeforces.com/api/{method}'


def getBlogEntryComments(blogEntryId: int) -> List[Comment]:
    METHOD = f'blogEntry.comments?blogEntryId={blogEntryId}'
    pass


def getBlogEntryView(blogEntryId: int) -> BlogEntry:
    METHOD = f'blogEntry.view?blogEntryId={blogEntryId}'
    pass


def getContestHacks(contestId: int, asManager: bool = False) -> List[Hack]:
    METHOD = f'contest.hacks?contestId={contestId}&asManager={asManager}'
    pass


def getContestList(gym: bool = False) -> List[Contest]:
    METHOD = f'contest.list?gym={gym}'
    pass


def getContestRatingChanges(contestId: int) -> List[RatingChange]:
    METHOD = f'contest.ratingChanges?contestId={contestId}'
    pass


class ContestStandings(TypedDict):
    contest: Contest
    problems: List[Problem]
    rows: List[RanklistRow]


def getContestStandings(contestId: int, from_: int, count: int, handles: List[str], room: str = None, showUnofficial: bool = False, asManager: bool = False) -> ContestStandings:
    pass


def getContestStatus(contestId: int, handle: str, from_: int, count: int, asManager: bool = False) -> List[Submission]:
    pass


def getProblemsetProblems(tags: List[str], problemsetName: str) -> Tuple[List[Problem], List[ProblemStatistics]]:
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


def getUserRatedList(activeOnly: bool, includeRetired: bool, contestId: int) -> List[User]:
    pass


def getUserRating(handle: str) -> List[RatingChange]:
    pass


def getUserStatus(handle: str, from_: int, count: int) -> List[Submission]:
    pass