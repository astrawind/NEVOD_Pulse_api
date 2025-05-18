from datetime import datetime, time
from src.database import MongoConnectionMaker

class EASRepository:
    
    def __init__(self, connection_maker: MongoConnectionMaker):
        self.get_connection = connection_maker
    
    def get_quality_rates(self, left_time_range: datetime, right_time_range: datetime):
        db = self.get_connection()
        date_prefix = f'{left_time_range}'[:10]
        collection = db[f'2022-12-28_e']
        min_time = left_time_range - datetime.combine(left_time_range.date(), time())
        min_time_ns = min_time.total_seconds() * 1000000000
        max_time = right_time_range - datetime.combine(right_time_range.date(), time())
        max_time_ns = max_time.total_seconds() * 1000000000
        pipeline = [
     {
        "$match": {
        "time_ns": {
        "$gte": min_time_ns,
        "$lte": max_time_ns
  }
}

    },
     {
        "$group": {
            "_id": "$cluster",
            "total": {"$sum": 1},
            "good": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$quality", "good"]},
                        1,
                        0
                    ]
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "cluster": "$_id", 
            "value": {"$divide": ["$good", "$total"]}
        }
    }
                ]
        result = list(collection.aggregate(pipeline))
        if result:
            return result
        else:
            return None

    