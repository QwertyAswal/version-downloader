import requests
import os

end_line = '\n'+'*' * os.get_terminal_size().columns+'\n'
wait_line = 'Please wait while program is loading..........\n'

print('\nThe following program downloads the last added binary file from a git repo.')
print(end_line)

try:
    choice = int(
        input('Input 1 for public repository and 2 for private repository: '))
    print(end_line)
    if choice != 1 and choice != 2:
        raise Exception()
except Exception:
    print('Enter Valid Choice\n')
    exit()
try:

    repository_name = input('Enter repository name: ')
    username = input('Enter user name of the repository: ')
    if choice == 2:
        access_token = 'token ' + \
            input('Enter personal access token of the repository: ')

    print(end_line)
    print(wait_line)

    url_releases = 'https://api.github.com/repos/{}/{}/releases'.format(
        username, repository_name)

    headers_release = {
        'Accept': 'application/json'
    }

    if choice == 2:
        headers_release['Authorization'] = access_token

    data = requests.get(url=url_releases, headers=headers_release).json()

    tags = {}

    for i in data:
        temp_urls = []
        for j in i['assets']:
            temp_urls.append({'url': j['url'], 'name': j['name']})
        tags[str(i['tag_name'])] = temp_urls

    print('The following versions were found -', ', '.join(tags))

    tag = input('Enter the selected version: ')

    if tag not in tags.keys():
        print(end_line)
        print('Enter a valid version name\n')
        exit()
    else:
        print(end_line)
        to_download = tags[tag]
        dir_name = 'version_'+tag
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        print('Files downloading: ')
        for i in to_download:
            url = i['url']
            name = i['name']

            print(name+'- ', end='')

            headers = {
                'Accept': 'application/octet-stream'
            }

            if choice == 2:
                headers['Authorization'] = access_token

            try:
                if not os.path.exists(dir_name+'/'+name):
                    r = requests.get(url, headers=headers)
                    f = open(dir_name+'/'+name, 'wb')
                    for chunk in r.iter_content(chunk_size=512 * 1024):
                        if chunk:
                            f.write(chunk)
                    f.close()
                    print('DOWNLOADED')
                else:
                    print('ALREADY PRESENT')
            except Exception:
                print('NOT DOWNLOADED')
        print(end_line)
        print('Download Completed\n')
except Exception:
    print('Error Occured\n')
