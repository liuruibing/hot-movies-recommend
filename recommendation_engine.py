import json
import random
from datetime import datetime
from typing import List, Dict, Any


class RecommendationEngine:
    """
    影视推荐引擎
    基于热度、评分、类型等因素进行推荐
    """
    
    def __init__(self):
        # 加载基础数据，这里我们使用从API获取的数据作为基础
        self.movies_data = {}
        
    def calculate_recommendation_score(self, movie: Dict[str, Any]) -> float:
        """
        计算推荐分数
        综合考虑评分、热度、更新时间等因素
        """
        score = float(movie.get('vod_score', 0) or 0)
        
        # 热度影响因子 (vod_hits)
        hits = int(movie.get('vod_hits', 0) or 0)
        if hits > 10000:
            score += 2.0
        elif hits > 5000:
            score += 1.5
        elif hits > 1000:
            score += 1.0
        
        # 评分权重调整
        if score > 0:
            score *= 1.2  # 对有评分的项目增加权重
            
        # 类型偏好（随机性添加一些多样性）
        genre_factor = random.uniform(0.8, 1.2)
        score *= genre_factor
        
        # 防止分数过高溢出
        return min(score, 10.0)
    
    def get_trending_movies(self, movies: List[Dict[str, Any]], limit: int = 4) -> List[Dict[str, Any]]:
        """
        获取热门电影/电视剧
        """
        # 过滤有效数据并计算推荐分数
        valid_movies = []
        for movie in movies:
            if movie.get('vod_name') and movie.get('vod_pic'):
                movie['recommendation_score'] = self.calculate_recommendation_score(movie)
                valid_movies.append(movie)
        
        # 按推荐分数排序
        sorted_movies = sorted(valid_movies, key=lambda x: x['recommendation_score'], reverse=True)
        return sorted_movies[:limit]
    
    def get_personalized_recommendations(self, movies: List[Dict[str, Any]], 
                                       preferred_genres: List[str] = None, 
                                       limit: int = 4) -> List[Dict[str, Any]]:
        """
        获取个性化推荐
        """
        if not preferred_genres:
            # 如果没有指定偏好，则使用趋势推荐
            return self.get_trending_movies(movies, limit)
        
        # 根据偏好类型过滤
        filtered_movies = []
        for movie in movies:
            if not movie.get('vod_name') or not movie.get('vod_pic'):
                continue
                
            # 检查是否匹配偏好类型
            vod_class = movie.get('vod_class', '')
            match_found = False
            for genre in preferred_genres:
                if genre.lower() in vod_class.lower():
                    match_found = True
                    break
                    
            if match_found:
                movie['recommendation_score'] = self.calculate_recommendation_score(movie)
                filtered_movies.append(movie)
        
        # 如果没有找到匹配的类型，则返回趋势推荐
        if not filtered_movies:
            return self.get_trending_movies(movies, limit)
            
        # 按推荐分数排序
        sorted_movies = sorted(filtered_movies, key=lambda x: x['recommendation_score'], reverse=True)
        return sorted_movies[:limit]
    
    def get_diversified_recommendations(self, movies: List[Dict[str, Any]], 
                                      limit: int = 4) -> List[Dict[str, Any]]:
        """
        获取多样化推荐（避免重复类型）
        """
        valid_movies = []
        for movie in movies:
            if movie.get('vod_name') and movie.get('vod_pic'):
                movie['recommendation_score'] = self.calculate_recommendation_score(movie)
                valid_movies.append(movie)
        
        # 按推荐分数排序
        sorted_movies = sorted(valid_movies, key=lambda x: x['recommendation_score'], reverse=True)
        
        # 选择不同类型的影片以增加多样性
        selected_movies = []
        used_genres = set()
        
        for movie in sorted_movies:
            if len(selected_movies) >= limit:
                break
                
            # 尝试按类型区分
            vod_class = movie.get('vod_class', '').lower()
            primary_genre = vod_class.split(',')[0] if vod_class else 'unknown'
            
            # 如果类型未被使用过，或者我们还没有足够的推荐，则添加
            if primary_genre not in used_genres or len(used_genres) < 2:
                selected_movies.append(movie)
                used_genres.add(primary_genre)
            elif len(selected_movies) < limit:  # 如果还有空位，添加任何剩余的高分项
                selected_movies.append(movie)
        
        return selected_movies[:limit]


# 创建推荐引擎实例
recommendation_engine = RecommendationEngine()