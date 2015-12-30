import numpy as np,argparse,pickle
from qa_tuple import *

def train_model(tuples,n_iter,learning_rate,qvecs):
    iter = 0
    W = np.identity(100)
    error_old = np.inf
    while True:
        index = np.random.randint(0,len(tuples))
        # print index
        tuple = tuples[index]
        qvec = qvecs[tuple.q].qvec
        C = 1-np.transpose(qvec)*W*tuple.plus+np.transpose(qvec)*W*tuple.minus
        if C > 0:
            # print tuple.q*np.transpose(tuple.plus)
            # print tuple.q*np.transpose(tuple.plus)
            d = learning_rate*(qvec*np.transpose(tuple.plus)-qvec*np.transpose(tuple.minus))
            W = W + d
        else:
            continue
        error = compute_error(tuples,W)
        if error >= error_old or iter == n_iter:
            break
        iter = iter + 1
        error_old = error
    print error
    # print iter
    return W

def compute_error(tuples,W,q_dict):
    return sum([max(0,1-np.transpose(q_dict[t.q].qvec)*W*t.plus+np.transpose(q_dict[t.q].qvec)*W*t.minus) for t in tuples])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train doc2vec.")
    parser.add_argument("fname",help="filename",type=str)
    parser.add_argument("model",help="modelname",type=str)
    parser.add_argument("a_model",help="answer modelname",type=str)
    parser.add_argument("n_iter",help="number of iterations",type=int)
    parser.add_argument("alpha",help="learning rate",type=float)
    args = parser.parse_args()
    # q = load_questions(args.model,args.fname,"doc_mapper.txt",args.a_model)
    with open("questions_objects") as h:
        q = pickle.load(h)
    with open("qa_tuples.pickle") as f:
        t = pickle.load(f)
    # t = load_tuples(q)
    W = train_model(t,args.n_iter,args.alpha,create_q_dict(q))
    with open("SSI_"+str(args.n_iter)+"_"+str(args.alpha)+".pickle","wb") as g:
        pickle.dump(W,g)