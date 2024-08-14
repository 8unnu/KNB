from database.database import async_factory
from database.models import User, Score

from sqlalchemy.future import select

async def pg_game_operation(result, completed_id):
    async with async_factory() as session:
        score_result = Score(user_id=completed_id, result=result)
        session.add(score_result)
        await session.commit()

async def pg_user_create(username, password):
    async with async_factory() as session:
        user = User(username=username, password=password)
        session.add(user)
        await session.commit()

async def pg_get_all_usernames():
    async with async_factory() as session:
        query = select(User.username)
        result = await session.execute(query)
        users = result.fetchall()
        return users

async def pg_get_user_id(username):
    async with async_factory() as session:
        query = select(User.id).filter_by(username=username)
        result = await session.execute(query)
        user_id = result.fetchall()
        return user_id

async def pg_get_user_password(username):
    async with async_factory() as session:
        query = select(User.password).filter_by(username=username)
        result = await session.execute(query)
        user_password = result.fetchall()
        return user_password

async def pg_get_games_results(completed_id):
    async with async_factory() as session:
        query = select(Score.result).filter_by(user_id=completed_id)
        result = await session.execute(query)
        games_results = result.fetchall()
        return games_results

async def pg_get_games_results_wins(completed_id):
    async with async_factory() as session:
        query = select(Score.result).filter_by(user_id=completed_id, result=1)
        result = await session.execute(query)
        games_results = result.fetchall()
        return len(games_results)

async def pg_get_games_results_loses(completed_id):
    async with async_factory() as session:
        query = select(Score.result).filter_by(user_id=completed_id, result=0)
        result = await session.execute(query)
        games_results = result.fetchall()
        return len(games_results)