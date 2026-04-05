# from fastapi import Request, HTTPException, status, Depends
# from app.core.redis import redis_client

# def rate_limit(max_requests: int, window_seconds: int):
#     """
#     Dependency factory for rate limiting.
#     """

#     async def limiter(request: Request):
#         user = getattr(request.state, "user", None)

#         if user:
#             identifier = f"user:{user.id}"
#         else:
#             identifier = f"ip:{request.client.host}"

#         key = f"rate_limit:{identifier}:{request.url.path}"

#         current = await redis_client.get(key)

#         if current and int(current) >= max_requests:
#             raise HTTPException(
#                 status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#                 detail="Rate limit exceeded. Try again later.",
#             )

#         pipe = redis_client.pipeline()

#         pipe.incr(key)

#         if not current:
#             pipe.expire(key, window_seconds)

#         await pipe.execute()

#     return limiter

# async def global_rate_limit(request: Request):
#     identifier = f"ip:{request.client.host}"
#     key = f"global_rate:{identifier}"

#     current = await redis_client.get(key)

#     if current and int(current) >= 100:
#         raise HTTPException(429, "Too many requests")

#     pipe = redis_client.pipeline()
#     pipe.incr(key)

#     if not current:
#         pipe.expire(key, 60)

#     await pipe.execute()