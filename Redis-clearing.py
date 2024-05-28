import redis
import os

# Get the Redis password from the environment variable
redis_password = os.getenv('REDIS_PASSWORD')

# Check if the environment variable is set
if redis_password is None:
    raise ValueError("The REDIS_PASSWORD environment variable is not set.")

r = redis.Redis(
    host='kudaglobal-prod.redis.cache.windows.net',
    port=6379,
    password=redis_password,
    decode_responses=True
)

# Check for pending messages
rkeys = r.keys()
for i in rkeys:
    keyr = (r.keys(i))
    stlen = (r.xlen(i))
    pendingc = r.execute_command("XINFO GROUPS", i)
    for j in range(len(pendingc)):
        list4 = [d.get('pending') for d in pendingc]
    Tpend = sum(list4)
    cleared = abs(int(stlen - Tpend))
    r.xtrim(i, approximate=False, maxlen=str(abs(Tpend)))
