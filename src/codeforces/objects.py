from enum import Enum, auto
from typing import List, Optional

from pydantic import (BaseModel, Field, HttpUrl, NonNegativeFloat,
                      NonNegativeInt, PositiveFloat, PositiveInt, StrictInt)


class User(BaseModel):
    handle: str
    email: str
    vkId: str
    openId: str
    firstName: Optional[str]
    lastNam: Optional[str]
    country: Optional[str]
    city: Optional[str]
    organization: Optional[str]
    contribution: StrictInt
    rank: str
    rating: StrictInt
    maxRank: str
    maxRating: StrictInt
    lastOnlineTimeSeconds: NonNegativeInt
    registrationTimeSeconds: NonNegativeInt
    friendOfCount: NonNegativeInt
    avatar: HttpUrl
    titlePhoto: HttpUrl


class BlogEntry(BaseModel):
    id: int
    originalLocale: str
    creationTimeSeconds: NonNegativeInt
    authorHandle: str
    title: str
    content: str
    locale: str
    modificationTimeSeconds: NonNegativeInt
    allowViewHistory: bool
    tags: List[str]
    rating: StrictInt


class Comment(BaseModel):
    id: int
    creationTimeSeconds: NonNegativeInt
    commentatorHandle: str
    locale: str
    text: str
    parentCommentId: Optional[int]
    rating: NonNegativeInt


class RecentAction(BaseModel):
    timeSeconds: NonNegativeInt
    blogEntry: BlogEntry
    comment: Comment


class RatingChange(BaseModel):
    contestId: int
    contestName: str
    handle: str
    rank: PositiveInt
    ratingUpdateTimeSeconds: NonNegativeInt
    oldRating: NonNegativeInt
    newRating: NonNegativeInt


class ContestType(str, Enum):
    CF = auto()
    IOI = auto()
    ICPC = auto()


class ContestPhase(str, Enum):
    BEFORE = auto()
    CODING = auto()
    PENDING_SYSTEM_TEST = auto()
    SYSTEM_TEST = auto()
    FINISHED = auto()


class Contest(BaseModel):
    id: int
    name: str
    type: ContestType
    phase: ContestPhase
    frozen: bool
    durationSeconds: NonNegativeInt
    startTimeSeconds: Optional[NonNegativeInt]
    relativeTimeSeconds: Optional[StrictInt]
    preparedBy: Optional[str]
    websiteUrl: Optional[HttpUrl]
    description: Optional[str]
    difficulty: Optional[int] = Field(ge=1, le=5)
    kind: Optional[str] = Field(
        pattern=r'Official ICPC Contest|Official School Contest|Opencup Contest|School/University/City/Region Championship|Training Camp Contest|Official International Personal Contest|Training Contest')
    icpcRegion: Optional[str]
    country: Optional[str]
    city: Optional[str]
    season: Optional[str]


class Party(BaseModel):
    pass


class Member(BaseModel):
    pass


class ProblemType(str, Enum):
    PROGRAMMING = auto()
    QUESTION = auto()


class Problem(BaseModel):
    contestId: Optional[int]
    problemsetName: Optional[str]
    index: str
    name: str
    type: ProblemType
    points: Optional[PositiveFloat]
    rating: Optional[int] = Field(ge=1, le=5)
    tags: List[str]


class ProblemStatistics(BaseModel):
    contestId: Optional[int]
    index: str
    solvedCount: NonNegativeInt


class Verdict(str, Enum):
    FAILED = auto()
    OK = auto()
    PARTIAL = auto()
    COMPILATION_ERROR = auto()
    RUNTIME_ERROR = auto()
    WRONG_ANSWER = auto()
    PRESENTATION_ERROR = auto()
    TIME_LIMIT_EXCEEDED = auto()
    MEMORY_LIMIT_EXCEEDED = auto()
    IDLENESS_LIMIT_EXCEEDED = auto()
    SECURITY_VIOLATED = auto()
    CRASHED = auto()
    INPUT_PREPARATION_CRASHED = auto()
    CHALLENGED = auto()
    SKIPPED = auto()
    TESTING = auto()
    REJECTED = auto()


class TestSet(str, Enum):
    SAMPLES = auto()
    PRETESTS = auto()
    TESTS = auto()
    TESTS1 = auto()
    TESTS2 = auto()
    TESTS3 = auto()
    TESTS4 = auto()
    TESTS5 = auto()
    TESTS6 = auto()
    TESTS7 = auto()
    TESTS8 = auto()
    TESTS9 = auto()
    TESTS10 = auto()


class Submission(BaseModel):
    id: int
    contestId: Optional[int]
    creationTimeSeconds: Optional[NonNegativeInt]
    relativeTimeSeconds: int
    problem: Problem
    author: Party
    programmingLanguage: str
    verdict: Optional[Verdict]
    testset: TestSet
    passedTestCount: NonNegativeInt
    timeConsumedMillis: NonNegativeInt
    memoryConsumedBytes: NonNegativeInt
    points: Optional[NonNegativeFloat]


class Hack(BaseModel):
    pass


class RanklistRow(BaseModel):
    pass


class ProblemResult(BaseModel):
    pass
