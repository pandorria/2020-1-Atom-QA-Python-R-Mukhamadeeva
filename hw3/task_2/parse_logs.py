import os
import argparse
import json

from client import MysqlConnection

db = MysqlConnection(user='root', password='123456', db_name='logs', delete=False)


def parse_logs(log_path, top=10):
    total = 0
    requests_type = {'GET': 0, 'HEAD': 0, 'POST': 0, 'PUT': 0, 'DELETE': 0, 'CONNECT': 0, 'OPTIONS': 0, 'TRACE': 0}
    top_largest_requests = []
    top_client_errors = []
    top_redirect_requests = []
    with open(log_path) as file:
        for line in file:
            total += 1
            split_line = line.strip().split()
            requests_type[split_line[5][1:]] += 1
            top_largest_requests.append([split_line[9], split_line[6], int(split_line[8])])
            if len(top_client_errors) <= top and 399 < int(split_line[8]) < 500:
                top_client_errors.append([split_line[6], int(split_line[8]), split_line[0]])
            if len(top_redirect_requests) <= top and 299 < int(split_line[8]) < 400:
                top_redirect_requests.append([split_line[6], int(split_line[8]), split_line[0]])
    db.execute_query('INSERT INTO Total_Requests (count) VALUES ({})'.format(total))
    for key, value in requests_type.items():
        if value > 0:
            db.execute_query('INSERT INTO Request_Methods (http_type, count) VALUES ("{}", {})'.format(key, value))
    top_largest_requests.sort(key=lambda i: i[0])
    for i in range(top):
        db.execute_query('INSERT INTO Lagest_Requests (request_size, url,  request_code) VALUES ({}, "{}", "{}")'.format(top_largest_requests[i][0], top_largest_requests[i][1], top_largest_requests[i][2]))
    for i in top_client_errors:
        db.execute_query('INSERT INTO Client_Errors (IP, url,  request_code) VALUES ("{}", "{}", {})'.format(i[2], i[0], i[1]))
    for i in top_redirect_requests:
        db.execute_query(
            'INSERT INTO Redirect_Requests (IP, url,  request_code) VALUES ("{}", "{}", {})'.format(i[2], i[0], i[1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=None)
    parser.add_argument('--dir', type=str, default=None)
    parser.add_argument('--top', type=int, default=10)
    args = parser.parse_args()

    if args.dir:
        for name in os.listdir(args.dir):
            parse_logs(os.path.join(args.dir, name), args.top)
    else:
        parse_logs(args.file, args.top)
