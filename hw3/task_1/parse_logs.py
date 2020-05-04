import os
import argparse
import json


def parse_logs(log_path, result, save_json=False, top=10):
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
            top_largest_requests.append([split_line[9], split_line[6], split_line[8]])
            if len(top_client_errors) <= top and 399 < int(split_line[8]) < 500:
                top_client_errors.append([split_line[6], split_line[8], split_line[0]])
            if len(top_redirect_requests) <= top and 299 < int(split_line[8]) < 400:
                top_redirect_requests.append([split_line[6], split_line[8], split_line[0]])
    with open('{}.txt'.format(result), 'w') as file:
        file.write("Total Requests:\n")
        file.write(str(total))
        file.write("\nTotal Request Methods:\n")
        for key, value in requests_type.items():
            if value > 0:
                file.write('{} - {}\n'.format(key, value))
        file.write("Top 10 Lagest Requests:\n")
        top_largest_requests.sort(key=lambda i: i[0])
        for i in range(top):
            file.write(
                '{} {} {}\n'.format(top_largest_requests[i][0], top_largest_requests[i][1], top_largest_requests[i][2]))
        file.write("Top 10 Client Error:\n")
        for i in top_client_errors:
            file.write('{} {} {}\n'.format(i[0], i[1], i[2]))
        for i in top_redirect_requests:
            file.write('{} {} {}\n'.format(i[0], i[1], i[2]))
    if save_json:
        with open('{}.json'.format(result), 'w') as file:
            json.dump({
                'total': total,
                'requests_type': requests_type,
                'top_largest': top_largest_requests[:top],
                'top_client_errors': top_client_errors,
                'top_redirect': top_redirect_requests
            }, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=None)
    parser.add_argument('--dir', type=str, default=None)
    parser.add_argument('--json', type=int, default=0)
    parser.add_argument('--top', type=int, default=10)
    args = parser.parse_args()

    if args.dir:
        for name in os.listdir(args.dir):
            parse_logs(os.path.join(args.dir, name), name, args.json, args.top)
    else:
        parse_logs(args.file, args.file, args.json, args.top)
