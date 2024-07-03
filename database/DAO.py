from database.DB_connect import DBConnect
from model.connessa import Connessa
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT gp.Product_color 
                    from go_products gp """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["Product_color"])

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getProducts(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM go_products gp
                    WHERE gp.Product_color = %s """

        cursor.execute(query, (color, ))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getConnessa(idMap, color, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT Prod1.Product_number as Product1, Prod2.Product_number as Product2
                    FROM(SELECT *
                        from go_products gp 
                        WHERE gp.Product_color = %s) as Prod1,
                        (SELECT *
                        from go_products gp 
                        WHERE gp.Product_color = %s) as Prod2,
                        (SELECT *
                        FROM go_daily_sales gds 
                        WHERE year(gds.`Date`)= %s) as Vend1,
                        (SELECT *
                        FROM go_daily_sales gds 
                        WHERE year(gds.`Date`)= %s) as Vend2
                    WHERE Vend1.Retailer_code = Vend2.Retailer_code AND Vend1.Date = Vend2.Date AND Prod1.Product_number != Prod2.Product_number AND Prod1.Product_number = Vend1.Product_number AND Prod2.Product_number = Vend2.Product_number AND Prod1.Product_number < Prod2.Product_number
                    GROUP By Prod1.Product_number, Prod2.Product_number """

        cursor.execute(query, (color,color,year,year))

        for row in cursor:
            result.append(Connessa(idMap[row["Product1"]], idMap[row["Product2"]], 0))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getPeso(prod1, prod2, color, year):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """ 
                SELECT COUNT(DISTINCT gds2.Date) as Peso
                FROM go_daily_sales gds , go_daily_sales gds2 , go_products gp 
                WHERE gds.Product_number = %s AND gds2.Product_number = %s AND gds.Retailer_code = gds2.Retailer_code AND gds.`Date` = gds2.`Date` AND year(gds2.`Date`) = %s and gp.Product_number = gds2.Product_number and gp.Product_color = %s """

        cursor.execute(query, (prod1, prod2, year, color))

        for row in cursor:
            result = row["Peso"]

        cursor.close()
        conn.close()

        return result

