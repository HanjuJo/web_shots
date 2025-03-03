from datetime import datetime
import sqlite3
import json

class CommunityManager:
    def __init__(self):
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        # 게시글 테이블
        c.execute('''CREATE TABLE IF NOT EXISTS posts
                    (id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    view_count INTEGER DEFAULT 0,
                    like_count INTEGER DEFAULT 0,
                    comment_count INTEGER DEFAULT 0,
                    tags TEXT,
                    images TEXT,
                    FOREIGN KEY(author_id) REFERENCES users(id))''')
                    
        # 댓글 테이블
        c.execute('''CREATE TABLE IF NOT EXISTS comments
                    (id INTEGER PRIMARY KEY,
                    post_id INTEGER NOT NULL,
                    author_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    parent_id INTEGER,
                    like_count INTEGER DEFAULT 0,
                    FOREIGN KEY(post_id) REFERENCES posts(id),
                    FOREIGN KEY(author_id) REFERENCES users(id),
                    FOREIGN KEY(parent_id) REFERENCES comments(id))''')
                    
        # 좋아요 테이블
        c.execute('''CREATE TABLE IF NOT EXISTS likes
                    (id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    post_id INTEGER,
                    comment_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(post_id) REFERENCES posts(id),
                    FOREIGN KEY(comment_id) REFERENCES comments(id))''')
                    
        conn.commit()
        conn.close()
        
    def create_post(self, user_id, title, content, category, tags=None, images=None):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO posts 
                        (title, content, category, author_id, tags, images)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (title, content, category, user_id,
                      json.dumps(tags) if tags else None,
                      json.dumps(images) if images else None))
            
            post_id = c.lastrowid
            conn.commit()
            
            # 새로 생성된 게시글 정보 반환
            c.execute('''SELECT p.*, u.username, u.avatar
                        FROM posts p
                        JOIN users u ON p.author_id = u.id
                        WHERE p.id = ?''', (post_id,))
            
            post = c.fetchone()
            return self._format_post(post)
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def get_posts(self, page=1, per_page=20, category=None, search=None, sort_by='latest'):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            query = '''SELECT p.*, u.username, u.avatar,
                             COUNT(DISTINCT c.id) as comment_count,
                             COUNT(DISTINCT l.id) as like_count
                      FROM posts p
                      JOIN users u ON p.author_id = u.id
                      LEFT JOIN comments c ON c.post_id = p.id
                      LEFT JOIN likes l ON l.post_id = p.id
                      WHERE 1=1'''
            params = []
            
            if category:
                query += ' AND p.category = ?'
                params.append(category)
                
            if search:
                query += ' AND (p.title LIKE ? OR p.content LIKE ?)'
                search_term = f'%{search}%'
                params.extend([search_term, search_term])
                
            query += ' GROUP BY p.id'
            
            # 정렬
            if sort_by == 'popular':
                query += ' ORDER BY like_count DESC'
            elif sort_by == 'views':
                query += ' ORDER BY p.view_count DESC'
            else:  # latest
                query += ' ORDER BY p.created_at DESC'
                
            # 페이지네이션
            query += ' LIMIT ? OFFSET ?'
            params.extend([per_page, (page - 1) * per_page])
            
            c.execute(query, params)
            posts = c.fetchall()
            
            # 전체 게시글 수 계산
            count_query = query.split('GROUP BY')[0].replace('SELECT p.*, u.username, u.avatar', 'SELECT COUNT(DISTINCT p.id)')
            c.execute(count_query, params[:-2])  # 페이지네이션 파라미터 제외
            total_count = c.fetchone()[0]
            
            return {
                'posts': [self._format_post(post) for post in posts],
                'total': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page
            }
            
        finally:
            conn.close()
            
    def get_post(self, post_id, user_id=None):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            # 조회수 증가
            c.execute('UPDATE posts SET view_count = view_count + 1 WHERE id = ?', (post_id,))
            
            # 게시글 정보 조회
            c.execute('''SELECT p.*, u.username, u.avatar,
                               COUNT(DISTINCT c.id) as comment_count,
                               COUNT(DISTINCT l.id) as like_count,
                               EXISTS(SELECT 1 FROM likes WHERE post_id = p.id AND user_id = ?) as is_liked
                        FROM posts p
                        JOIN users u ON p.author_id = u.id
                        LEFT JOIN comments c ON c.post_id = p.id
                        LEFT JOIN likes l ON l.post_id = p.id
                        WHERE p.id = ?
                        GROUP BY p.id''',
                     (user_id, post_id))
            
            post = c.fetchone()
            if not post:
                return None
                
            # 댓글 조회
            c.execute('''SELECT c.*, u.username, u.avatar,
                               COUNT(l.id) as like_count,
                               EXISTS(SELECT 1 FROM likes WHERE comment_id = c.id AND user_id = ?) as is_liked
                        FROM comments c
                        JOIN users u ON c.author_id = u.id
                        LEFT JOIN likes l ON l.comment_id = c.id
                        WHERE c.post_id = ?
                        GROUP BY c.id
                        ORDER BY c.created_at DESC''',
                     (user_id, post_id))
            
            comments = c.fetchall()
            
            conn.commit()
            
            result = self._format_post(post)
            result['comments'] = [self._format_comment(comment) for comment in comments]
            return result
            
        finally:
            conn.close()
            
    def create_comment(self, user_id, post_id, content, parent_id=None):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO comments 
                        (post_id, author_id, content, parent_id)
                        VALUES (?, ?, ?, ?)''',
                     (post_id, user_id, content, parent_id))
            
            comment_id = c.lastrowid
            
            # 게시글의 댓글 수 증가
            c.execute('UPDATE posts SET comment_count = comment_count + 1 WHERE id = ?', (post_id,))
            
            conn.commit()
            
            # 새로 생성된 댓글 정보 반환
            c.execute('''SELECT c.*, u.username, u.avatar
                        FROM comments c
                        JOIN users u ON c.author_id = u.id
                        WHERE c.id = ?''', (comment_id,))
            
            comment = c.fetchone()
            return self._format_comment(comment)
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def toggle_like(self, user_id, post_id=None, comment_id=None):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            # 좋아요 존재 여부 확인
            if post_id:
                c.execute('SELECT id FROM likes WHERE user_id = ? AND post_id = ?',
                         (user_id, post_id))
                target_table = 'posts'
                target_id = post_id
            else:
                c.execute('SELECT id FROM likes WHERE user_id = ? AND comment_id = ?',
                         (user_id, comment_id))
                target_table = 'comments'
                target_id = comment_id
                
            like = c.fetchone()
            
            if like:
                # 좋아요 취소
                c.execute('DELETE FROM likes WHERE id = ?', (like[0],))
                c.execute(f'UPDATE {target_table} SET like_count = like_count - 1 WHERE id = ?',
                         (target_id,))
                is_liked = False
            else:
                # 좋아요 추가
                c.execute('''INSERT INTO likes (user_id, post_id, comment_id)
                           VALUES (?, ?, ?)''',
                        (user_id, post_id, comment_id))
                c.execute(f'UPDATE {target_table} SET like_count = like_count + 1 WHERE id = ?',
                         (target_id,))
                is_liked = True
                
            conn.commit()
            
            # 현재 좋아요 수 반환
            c.execute(f'SELECT like_count FROM {target_table} WHERE id = ?', (target_id,))
            like_count = c.fetchone()[0]
            
            return {
                'is_liked': is_liked,
                'like_count': like_count
            }
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def get_comments(self, post_id, page=1, per_page=20):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            # 총 댓글 수 조회
            c.execute('SELECT COUNT(*) FROM comments WHERE post_id = ?', (post_id,))
            total_count = c.fetchone()[0]
            
            # 댓글 조회
            c.execute('''SELECT c.*, u.username, u.avatar,
                               COUNT(l.id) as like_count
                        FROM comments c
                        JOIN users u ON c.author_id = u.id
                        LEFT JOIN likes l ON l.comment_id = c.id
                        WHERE c.post_id = ? AND c.parent_id IS NULL
                        GROUP BY c.id
                        ORDER BY c.created_at DESC
                        LIMIT ? OFFSET ?''',
                     (post_id, per_page, (page - 1) * per_page))
            
            comments = c.fetchall()
            
            # 대댓글 조회
            for comment in comments:
                c.execute('''SELECT c.*, u.username, u.avatar,
                                   COUNT(l.id) as like_count
                            FROM comments c
                            JOIN users u ON c.author_id = u.id
                            LEFT JOIN likes l ON l.comment_id = c.id
                            WHERE c.parent_id = ?
                            GROUP BY c.id
                            ORDER BY c.created_at ASC''',
                         (comment[0],))
                
                replies = c.fetchall()
                comment['replies'] = [self._format_comment(reply) for reply in replies]
            
            return {
                'comments': [self._format_comment(comment) for comment in comments],
                'total': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page,
                'has_more': page * per_page < total_count
            }
            
        finally:
            conn.close()

    def update_comment(self, comment_id, content):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            c.execute('''UPDATE comments 
                        SET content = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?''',
                     (content, comment_id))
            
            if c.rowcount == 0:
                raise Exception('Comment not found')
                
            conn.commit()
            
            # 업데이트된 댓글 정보 반환
            c.execute('''SELECT c.*, u.username, u.avatar,
                               COUNT(l.id) as like_count
                        FROM comments c
                        JOIN users u ON c.author_id = u.id
                        LEFT JOIN likes l ON l.comment_id = c.id
                        WHERE c.id = ?
                        GROUP BY c.id''',
                     (comment_id,))
            
            comment = c.fetchone()
            return self._format_comment(comment)
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete_comment(self, comment_id):
        conn = sqlite3.connect('creator_tool.db')
        c = conn.cursor()
        
        try:
            # 댓글이 속한 게시글 ID 조회
            c.execute('SELECT post_id FROM comments WHERE id = ?', (comment_id,))
            result = c.fetchone()
            if not result:
                raise Exception('Comment not found')
                
            post_id = result[0]
            
            # 대댓글 삭제
            c.execute('DELETE FROM comments WHERE parent_id = ?', (comment_id,))
            
            # 댓글 삭제
            c.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
            
            # 댓글 수 업데이트
            c.execute('''UPDATE posts 
                        SET comment_count = (
                            SELECT COUNT(*) 
                            FROM comments 
                            WHERE post_id = ?
                        )
                        WHERE id = ?''',
                     (post_id, post_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _format_post(self, post):
        return {
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'category': post[3],
            'author': {
                'id': post[4],
                'username': post[12],
                'avatar': post[13]
            },
            'created_at': post[5],
            'updated_at': post[6],
            'view_count': post[7],
            'like_count': post[8],
            'comment_count': post[9],
            'tags': json.loads(post[10]) if post[10] else [],
            'images': json.loads(post[11]) if post[11] else [],
            'is_liked': bool(post[15]) if len(post) > 15 else False
        }
        
    def _format_comment(self, comment):
        return {
            'id': comment[0],
            'post_id': comment[1],
            'author': {
                'id': comment[2],
                'username': comment[7],
                'avatar': comment[8]
            },
            'content': comment[3],
            'created_at': comment[4],
            'parent_id': comment[5],
            'like_count': comment[6],
            'is_liked': bool(comment[10]) if len(comment) > 10 else False
        }
