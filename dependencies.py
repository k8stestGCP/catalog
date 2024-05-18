from fastapi import Depends, HTTPException, status, Request
from auth import verify_user
from pubsub import request_verification, subscribe_to_topic

async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not provided"
        )
    token = token.split("Bearer ")[1]

    request_verification(token)
    result = await subscribe_to_topic()
    print(result)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User verification failed"
        )

    return result