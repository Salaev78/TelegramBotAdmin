from aiogram import Router

from .status import router as status_router
from .stats import router as stats_router
from .resetstats import router as resetstats_router
from .logs import router as logs_router
from .user import router as user_router
# from .group import router as group_router

router = Router()

router.include_router(status_router)
router.include_router(stats_router)
router.include_router(resetstats_router)
router.include_router(logs_router)
router.include_router(user_router)
# router.include_router(group_router)