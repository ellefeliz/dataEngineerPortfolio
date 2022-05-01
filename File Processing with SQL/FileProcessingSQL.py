########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "esantana6"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = " create table if not exists movies (id integer, title text,  score real); "
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "create table if not exists movie_cast (movie_id integer, cast_id integer, cast_name text, birthday text, popularity real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################

       ######################################################################

        cursor = connection.cursor()

        m_file = open(path, encoding="utf-8")
        rows = csv.reader(m_file)
        cursor.executemany("INSERT INTO movies (id, title, score) VALUES (?, ?, ?)", rows)
        connection.commit()

        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        
        ######################################################################

        c_file = open(path, encoding="utf-8")
        rows = csv.reader(c_file)

        cursor = connection.cursor()

        cursor.executemany("INSERT INTO movie_cast VALUES (?, ?, ?, ?, ?)", rows)

        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = """ create table if not exists cast_bio(
                                cast_id integer PRIMARY KEY,
                                cast_name text,
                                birthday text,
                                popularity real                 
                            ) WITHOUT ROWID;
        """
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = """ INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity)
                                   SELECT distinct cast_id, cast_name, birthday, popularity from movie_cast;
        """
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(*) FROM cast_bio;"

        cursor = connection.execute(sql)
        #print(cursor.fetchall())
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = """
                    CREATE INDEX movie_index ON movies(id);
        """
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = """
                    CREATE INDEX cast_index ON movie_cast(cast_id);
        """
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = """
                    CREATE INDEX cast_bio_index ON cast_bio(cast_id);
        """
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """
                select printf("%.2f",100.0 * count(*)/(select count(*) from movies)  ) from movies
                where lower(title) like '%war%'
                  and score > 50
        """
        ######################################################################
        cursor = connection.execute(part_c_sql)
        #printf("hi there, i=%d, pi=%.2f\n", i, pi)

        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = """SELECT cast_name, count(*) appearance_count
                        FROM movie_cast
                        where popularity > 10
                        group by cast_name
                        order by appearance_count desc, cast_name
                        limit 5
        """
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """
                    SELECT m.title movie_title,
                           printf("%.2f",m.score) movie_score, count(cast_id) cast_count
                    FROM movies m inner join movie_cast c on m.id = c.movie_id
                    group by movie_title, movie_score
                    order by m.score desc, cast_count asc, movie_title asc      
                    limit 5                               
        """
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """

                select cast_id, cast_name,  
                printf("%.2f",average_score) average_score from 
                (
                     SELECT c.cast_id, c.cast_name 
                    ,avg(m.score) average_score
                    ,COUNT(*) tot 
                     FROM movie_cast c
                     inner join (select * from movies m2 where score >= 25) m 
                     on c.movie_id = m.id
                     group by  c.cast_id, c.cast_name
                     HAVING tot > 2
                     ORDER by average_score desc, c.cast_name asc
                 )
                   limit 10
                                             
        """
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """
                CREATE VIEW good_collaboration as
                select a.cast_id cast_member_id1, 
                b.cast_id cast_member_id2, 
                count(*) movie_count,
                avg(a.score) average_movie_score
                from 
                    (
                        select movie_id, cast_id, m.score
                        from movie_cast mc join movies m on mc.movie_id = m.id 
                    ) a,
                    (
                        select movie_id, cast_id, m.score
                        from movie_cast mc join movies m on mc.movie_id = m.id 
                    ) b
                where a.movie_id = b.movie_id 
                and a.cast_id < b.cast_id
                group by a.cast_id, b.cast_id
                having count(*) >= 3
                  and avg(a.score) >= 40
                  and avg(b.score) >= 40
                
        """
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """
                select distinct s.cast_id, cb.cast_name, printf("%.2f",avg(average_movie_score)) collaboration_score
                    from 
                    (
                        select a.cast_member_id1 as cast_id, a.average_movie_score  average_movie_score
                        from good_collaboration a
                        union
                        select b.cast_member_id2, b.average_movie_score  average_movie_score 
                        from good_collaboration b
                    ) s
                    join cast_bio cb on s.cast_id = cb.cast_id 
                    group by s.cast_id, cb.cast_name
                    order by avg(average_movie_score) desc, cb.cast_name asc
                    limit 5
        """
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE if not exists movie_overview USING fts3(id integer, overview text)"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################

        c_file = open(path, encoding="utf-8")
        rows = csv.reader(c_file)

        cursor = connection.cursor()
        cursor.executemany("INSERT INTO movie_overview VALUES (?, ?)", rows)

        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = """select count(*) cnt from movie_overview mo 
                         where overview match 'fight' """
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = """
                        select count(*) cnt from movie_overview mo 
                        where overview match 'space NEAR/5 program'
        """
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            #print(line[0])
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    #try:
    print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
    print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
    print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    #except:
    #    print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
