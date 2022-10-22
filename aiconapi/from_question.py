from unicodedata import category
import numpy as np

class Question(object):
    def __init__(self, category_score,charactor_score,content=""):
        self.category_score = category_score
        self.charactor_score = charactor_score
        self.content=content
    def get_category_score(self,current_score,answer):
        current_score[answer,:] += self.category_score[:,answer]
        print("category_score added: ",self.category_score[:,answer])
        return current_score
    def get_charactor_score(self,current_score,answer):
        current_score[:,answer] += self.charactor_score[:,answer]
        print("charactor_score added: ",self.charactor_score[:,answer])
        return current_score


questions = [
    # q1
    Question(
        content="q1",
        category_score=np.array([
        [0,2,0,1,0,1], # 哺乳類
        [1,0,1,0,2,0], # 海の生き物
        [0,0,2,1,1,0], # 鳥
        [1,0,0,0,2,1],
        [2,1,0,0,0,1],
        [0,0,1,1,0,2],]),
        charactor_score=np.array([
        [0,0,1,2,1,0], #
        [1,2,1,0,0,0],
        [2,0,0,1,1,0],
        [1,0,0,1,0,2],
        [0,0,2,0,1,1],
        [0,1,0,0,2,1],]),
    ),
    # q2
    Question(
        content="q2",
        category_score=np.array([
        [1,0,0,0,2,0],
        [1,0,0,2,0,0],
        [0,2,1,0,0,0],
        [0,0,0,1,1,0],
        [0,2,1,0,0,0],
        [2,0,0,0,1,0],]),
        charactor_score=np.array([
        [2,0,1,0,0,0],
        [0,0,0,2,1,0],
        [1,0,2,0,0,0],
        [0,2,0,1,0,0],
        [0,0,0,1,2,0],
        [1,0,2,0,0,0],]),
    ),
    # q3
    Question(
        content="q3",
        category_score=np.array([
        [0,0,2,0,1,0],
        [2,0,0,1,0,0],
        [0,0,1,0,2,0],
        [2,1,0,0,0,0],
        [0,1,0,2,0,0],
        [1,2,0,0,1,0],]),
        charactor_score=np.array([
        [0,0,1,0,2,0],
        [2,0,1,0,0,0],
        [0,0,2,0,1,0],
        [2,1,0,0,0,0],
        [1,0,0,2,0,0],
        [0,1,0,0,2,0],]),
    ),
    # q4
    Question(
        category_score=np.array([
        [0,1,0,1,2,0],
        [2,0,0,0,1,1],
        [0,1,2,1,0,0],
        [1,2,0,0,1,0],
        [0,0,1,2,0,1],
        [1,1,0,0,0,2],]),
        charactor_score=np.array([
        [0,1,2,0,0,1],
        [0,0,0,2,1,1],
        [2,0,0,1,1,0],
        [0,0,0,2,1,1],
        [0,1,0,1,0,2],
        [1,0,1,0,2,0],]),
    ),
    # q5
    Question(
        category_score=np.array([
        [0,2,1,0,0,0],
        [0,1,0,2,0,0],
        [0,0,0,1,2,0],
        [2,0,0,0,1,0],
        [0,0,1,0,2,0],
        [1,0,2,0,0,0],]),
        charactor_score=np.array([
        [2,0,0,0,1,0],
        [0,0,2,1,0,0],
        [1,2,0,0,0,0],
        [0,0,1,2,0,0],
        [1,0,0,0,2,0],
        [1,2,0,0,0,0],]),
    ),
    # q6
    Question(
        category_score=np.array([
        [0,2,1,0,0,1],
        [0,0,2,1,1,0],
        [2,1,0,0,0,1],
        [0,1,2,0,1,0],
        [1,0,0,1,2,0],
        [1,0,0,1,0,2],]),
        charactor_score=np.array([
        [2,0,1,0,0,1],
        [1,2,0,0,0,1],
        [0,1,2,1,0,0],
        [0,0,1,1,2,0],
        [0,0,0,2,1,1],
        [1,0,0,0,1,2],]),
    ),
    # q7
    Question(
        category_score=np.array([
        [2,0,1,0,0,1],
        [1,2,0,1,0,0],
        [2,1,1,0,0,0],
        [1,0,0,0,1,2],
        [0,0,0,1,2,1],
        [0,1,2,0,1,0],]),
        charactor_score=np.array([
        [0,2,1,0,1,0],
        [1,0,2,0,0,1],
        [2,1,0,1,0,0],
        [0,1,0,2,0,1],
        [0,0,1,1,0,2],
        [1,0,0,1,2,0],]),
    ),
    ]

tags_all = [
    ['ライオン','トラ','チーター'],['シャチ','サメ','シロナガスクジラ'],['鷲','鷹'],['富士山','エベレスト'],['フェラーリ','スーパーカー'],['プロレスラー'],
    ['ネコ','チワワ','ハムスター'],['カメ','イルカ'],['ひよこ','すずめ'],['桜','つくし'],['ボーカロイド','ルービックキューブ'],['雲','なめこ'],
    ['犬','パンダ'],['ペンギン','カクレクマノミ'],['インコ','オウム'],['クワガタムシ','カブトムシ'],['ロボット','ジープ'],['ゴースト','パンプキン'],
    ['柴犬','サル'],['魚','トビウオ'],['フクロウ','鳩'],['世界樹','大木'],['歯車','パソコン'],['メガネ'],
    ['オオカミ'],['クジラ'],['カラス'],['カマキリ'],['アンドロイド'],['ビル'],
    ['ゴリラ','マンドリル'],['タコ'],['クジャク'],['ひまわり'],['メルセデス'],['本'],    
]


def calc_score(ans):
    current_score = np.zeros([6,6])
    for i,q in enumerate(questions):
        print(q.content)
        # print(current_score)
        current_score = q.get_category_score(current_score,ans[i])
        current_score = q.get_charactor_score(current_score,ans[i])
        print(current_score)
    return current_score
        
def get_tags(ans):
    score = calc_score(ans)
    main_objs = tags_all[score.argmax()]
    score_sum = score.sum()
    # print(main_objs)
    main_obj = main_objs[int(score_sum)%len(main_objs)]
    print(main_obj)
    return [main_obj]

if __name__=="__main__":
    answer = np.array([3,3,3,3,3,3,3])
    print("ans",answer)
    score = get_tags(answer)
    print(score)
    # print(score.argmax())
