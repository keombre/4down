import dbm, json, os
from urllib.request import urlopen

def download(url_, targ_):
    """
    Download file
    """
    file_ = url_[url_.rfind('/')+1:]

    if os.path.isfile(targ_ + '/' + file_):
        print('File', file_, 'alredy archived, skipping.')
        return True
    print('Downloading', file_)
    
    try:
        response_ = urlopen(url_)
        meta_ = response_.info()
        size_ = int(meta_.get_all("Content-Length")[0])
        with open(targ_+'/'+file_, 'wb') as ff_:
            count_ = 0
            while True:
                bb_ = int(count_*(60/size_))
                print("["+"="*bb_+" "*(60-bb_)+"] "+str(int(count_/size_*100))+"%",\
                    end="\r")
                chunk_ = response_.read(16 * 1024)
                count_ += len(chunk_)
                if not chunk_:
                    break
                ff_.write(chunk_)
        print()
    except KeyboardInterrupt:
        exit()
    except:
        print('Download error, skipping')
        try:
            os.remove(targ_+'/'+file_)
        except KeyboardInterrupt:
            exit()
        except:
            None

def get_files(url_):
    """
    Get information about giver thread
    """
    response_ = urlopen(url_)
    list_ = json.loads(response_.read().decode('utf-8'))

    return list_['posts']

def thread(board_, thread_, db_):
    """
    Thread cutting
    """
    files_ = get_files('http://a.4cdn.org/' + board_ + '/thread/' + thread_ + '.json')

    len_ = len(files_)
    cc_ = 1
    for post_ in files_:
        if not 'filename' in post_:
            continue
        db_[board_][thread_].append(post_)
        print(str(cc_) + '/' + str(len_))
        download('http://i.4cdn.org/' + board_ + '/' + str(post_['tim']) + post_['ext'],\
            'local/' + board_ + '/' + str(thread_))
        cc_ += 1
    print('Skipped', len_-cc_, 'posts. Archived', cc_, 'images from thread', thread_)

    return db_

def main():
    """
    Main
    """
    orgdb_ = dbm.open('local', 'c')
    if not 'main' in orgdb_:
        orgdb_['main'] = '{}'
    db_ = json.loads(orgdb_['main'].decode('utf-8'))

    board_ = input('Board: ')
    if not os.path.isdir('local/' + board_):
        os.mkdir('local/' + board_)

    if not board_ in db_:
        db_[board_] = {}

    thread_ = input('Thread: ')
    if not os.path.isdir('local/' + board_ + '/' + thread_):
        os.mkdir('local/' + board_ + '/' + thread_)

    if not thread_ in db_[board_]:
        db_[board_][thread_] = []
    orgdb_['main'] = json.dumps(thread(board_, thread_, db_))

if __name__ == "__main__":
    main()
