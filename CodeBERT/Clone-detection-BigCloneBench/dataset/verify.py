import json

if __name__ == '__main__':
    subs = []
    with open('./test_subs_gan_0_500.jsonl') as f:
        for idx, line in enumerate(f):
            print('idx: {}'.format(idx))
            line=line.strip()
            js = json.loads(line)
            subs.append(js['substitutes'])
    print('length of subs: {}'.format(len(subs)))