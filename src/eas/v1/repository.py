from datetime import datetime, time
from src.database import MongoConnectionMaker


class EASRepository:
    
    def __init__(self, connection_maker: MongoConnectionMaker):
        self.get_connection = connection_maker
    
    def get_quality_rates(self, left_time_range: datetime, right_time_range: datetime):
        db = self.get_connection()
        date_prefix = f'{left_time_range}'[:10]
        collection = db[f'{date_prefix}_e']
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
        
    def get_q_std_values(self, time: datetime):
            db = self.get_connection()
            date_prefix = f'{time}'[:10]
            collection = db[f'{date_prefix}_e']
            pipeline = [
                # Фильтрация документов
                {
                    "$match": {
                        "quality": "good",
                        "stations": {"$exists": True}
                    }
                },
                
                # Преобразование stations в массив пар ключ-значение
                {
                    "$project": {
                        "cluster": 1,
                        "ds_entries": {"$objectToArray": "$stations"}
                    }
                },
                
                # Развертывание массива для обработки каждой записи отдельно
                {
                    "$unwind": "$ds_entries"
                },
                
                # Извлечение номера DS из ключа (k) и фильтрация формата ds_*
                {
                    "$addFields": {
                        "ds_number": {
                            "$let": {
                                "vars": {
                                    "parts": {"$split": ["$ds_entries.k", "_"]}
                                },
                                "in": {
                                    "$cond": {
                                        "if": {"$and": [
                                            {"$eq": [{"$size": "$$parts"}, 2]},
                                            {"$eq": [{"$arrayElemAt": ["$$parts", 0]}, "ds"]}
                                        ]},
                                        "then": {"$toInt": {"$arrayElemAt": ["$$parts", 1]}},
                                        "else": None
                                    }
                                }
                            }
                        }
                    }
                },
                
                # Фильтрация только валидных DS-номеров и значений q_std >= 0
                {
                    "$match": {
                        "ds_number": {"$ne": None},
                        "ds_entries.v.q_std": {"$gte": 0}
                    }
                },
                
                # Группировка и сбор значений
                {
                    "$group": {
                        "_id": {
                            "cluster": "$cluster",
                            "ds_number": "$ds_number"
                        },
                        "values": {"$push": "$ds_entries.v.q_std"}
                    }
                },
                
                # Форматирование вывода
                {
                    "$project": {
                        "_id": 0,
                        "cluster": "$_id.cluster",
                        "ds": "$_id.ds_number",
                        "values": 1
                    }
                }
            ]

            result = list(collection.aggregate(pipeline))
            if result:
                return result
            else:
                return None
