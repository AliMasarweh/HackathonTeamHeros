import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="hackathon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
if connection.open:
    print("successfully connected ")
if __name__ == '__main__':
    with open('product.txt', 'r+') as coded_products:
        for line in coded_products.readlines():
            print(line)
            line_codes = line.strip('\n').split(' - ')
            try:
                with connection.cursor() as cursor:
                    query = f'INSERT into coded_products values("{line_codes[0]}","{line_codes[1]}")'
                    cursor.execute(query)
            except:
                print("Could insert stores into DB")
        connection.commit()


