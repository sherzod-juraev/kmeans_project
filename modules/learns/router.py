from typing import Annotated
from fastapi import APIRouter, status, Body
from kmeans_model import kmeans
from . import DataPost
from numpy import array

learn_router = APIRouter()

kmeans.k = 3

@learn_router.post(
    '/',
    summary='Kmeans training',
    status_code=status.HTTP_200_OK,
    response_model=list[list[float]]
)
async def kmeans_fit(
        learn_data_array: list[DataPost]
) -> list[list[float]]:

    length = len(learn_data_array)
    learn_data = [0 for _ in range(length)]
    for i in range(length):
        learn_data[i] = array(learn_data_array[i].array)
    # malumotlarga moslashtirish
    kmeans.fit(learn_data)
    # markazlarni list tarzida qaytarish
    return kmeans.centers.tolist()

@learn_router.post(
    '/predict',
    summary='Kmeans predict',
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def kmeans_predict(
        array: Annotated[list[float], Body()]
) -> dict:
    predict_dict = {
        'center': int(kmeans.predict(array))
    }
    return predict_dict