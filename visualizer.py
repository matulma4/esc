import matplotlib.pyplot as plt
from bokeh.plotting import figure,output_file,show
from gensim import models

def visualize(model):
    X = [model[word][0] for word in model.vocab.keys()]
    Y = [model[word][1] for word in model.vocab.keys()]
    segments = [[] for seg in range(16)]
    labels = [word.decode('utf-8') for word in model.vocab.keys()]
    for x,y,label in zip(X,Y,labels):
        if x < 0.01:
            if y < 0.05:
                segments[15].append((x,y,label))
            elif y < 0.1:
                segments[9].append((x,y,label))
            elif y < 0.2:
                segments[10].append((x,y,label))
            elif y < 0.3:
                segments[11].append((x,y,label))
        elif x < 0.05:
            if y < 0.1:
                segments[12].append((x,y,label))
            elif y < 0.2:
                segments[13].append((x,y,label))
            elif y < 0.3:
                segments[14].append((x,y,label))
        elif x < 0.1:
            if y < 0.1:
                segments[0].append((x,y,label))
            elif y < 0.2:
                segments[1].append((x,y,label))
            elif y < 0.3:
                segments[2].append((x,y,label))
        elif x < 0.2:
            if y < 0.1:
                segments[3].append((x,y,label))
            elif y < 0.2:
                segments[4].append((x,y,label))
            elif y < 0.3:
                segments[5].append((x,y,label))
        elif x < 0.3:
            if y < 0.1:
                segments[6].append((x,y,label))
            elif y < 0.2:
                segments[7].append((x,y,label))
            elif y < 0.3:
                segments[8].append((x,y,label))


    for i in range(15):
        # output_file("bokeh\\"+str(i)+".html")
        # p = figure(plot_width=800,plot_height=600)
        # seg = segments[i]
        # # p.scatter(X[:100],Y[:100],marker="circle")
        # # labels = [word.decode('utf-8') for word in model.vocab.keys()]
        # for x, y, label in seg:
        #     p.text(float(x),float(y),text=[label],text_font_size="10pt")
        #     # pass
        # show(p)

    # plt.scatter(X, Y, alpha=0.5)
    # plt.plot(X,Y, 'k.', markersize=0.5)

        plt.figure(i)
        seg = segments[i]
        for x, y,label in seg:
            plt.annotate(label,(x, y))
    plt.show()

if __name__ == "__main__":
    model = models.Word2Vec("model5.word2vec")
    visualize(model)