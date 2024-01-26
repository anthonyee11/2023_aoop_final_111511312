

from skimage.filters import threshold_local
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
def documentScan(img):
    def ploter(image,si=[12,12]):
        fig, ax = plt.subplots(figsize=si);ax.imshow(image,cmap='gray')
        ax.get_xaxis().set_visible(False);ax.get_yaxis().set_visible(False)
        plt.show()

    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    nc,nr=gray.shape

    kernel = np.ones((5,5),np.uint8)
    dilation = cv.dilate(gray,kernel,iterations =5)
    blur =cv.GaussianBlur(dilation,(3,3),0)
    blur= cv.erode(blur,kernel,iterations =5)

    edge=cv.Canny(blur,70,210)
    ploter(edge)

    from itertools import combinations

    def getLineFunction(com):
        rho,theta=com
        a = np.cos(theta);b = np.sin(theta)
        x0 = a*rho;y0 = b*rho
        x1 = int(x0 + 1000*(-b));
        y1 = int(y0 + 1000*(a));
        x2 = int(x0 - 1000*(-b));
        y2 = int(y0 - 1000*(a));
        if(x2-x1!=0):
            mya=(y2-y1)/(x2-x1)
        else:
            mya=10000000000
        myb=y2-mya*x2
        return mya, myb

    def getLineDistance(a0,b0,a1,b1):
        sum1=0
        if((a0!=0)&(a1!=0)):
            for i in range(0,nc):
                sum1+=abs(((i-b0)/a0)-((i-b1)/a1))
        sum2=0;
        for i in range(0,nr):
            sum2+=abs((i*a0+b0)-(i*a1+b1))
        return min(sum1,sum2)
            
    t=100;j=0;c=0
    imgr=img.copy() 
    while(j<8 and c<30):     
        try:
            linesP=cv.HoughLines(edge,1,np.pi/180,t) 
            j=linesP.shape[0]
        except:       
            j=0
        c=c+1
        t=t-10
        

    lines=linesP.reshape(linesP.shape[0],2)
    t=0;c=0;lu=[]
    for l in lines:
        c=c+1;
        rho,theta=l
        for lt in lines[c:]:
            t=0
            if(lt[0]!=l[0]):
                rhot,thetat=lt        
                k=abs(lt-l)<[50,0.5] 
                
                if(k[0] and k[1]):
                    t=-1            
                    break                
        if(t==-1):  
            continue
        a = np.cos(theta);b = np.sin(theta)
        x0 = a*rho;y0 = b*rho
        x1 = int(x0 + 1000*(-b));
        y1 = int(y0 + 1000*(a));
        x2 = int(x0 - 1000*(-b));
        y2 = int(y0 - 1000*(a))
        imgr=cv.line(imgr.copy(),(x1,y1),(x2,y2),(0,0,255),2)
        lu.append(l)


    deleted=[];
    for item in list(combinations(lu,2)):
        if((list(item[0]) in deleted)| (list(item[1]) in deleted)):
            continue
        first=item[0][1]
        if(item[0][1]>(np.pi/2)):
            first=np.pi-item[0][1]
        second=item[1][1]
        if(item[1][1]>(np.pi/2)):
            second=np.pi-item[1][1]
        if(first-second<0.5):
            a0,b0=getLineFunction(item[0]);
            a1,b1=getLineFunction(item[1]);
            if(getLineDistance(a0,b0,a1,b1)<7500):
                deleted.append(list(item[0]))
                
    fix=0
    for i in range(0,len(lu)):
        if(list(lu[i-fix]) in deleted):
            lu.pop(i-fix)
            fix+=1
    ploter(imgr)
    lr=np.asarray(lu);
    j=np.reshape(lr,[lr.shape[0],1,2]);



    imgt=img.copy()
    def intersection(line1, line2):
        rho1, theta1 = line1
        rho2, theta2 = line2
        A = np.array([[np.cos(theta1), np.sin(theta1)],[np.cos(theta2), np.sin(theta2)]])
        b = np.array([[rho1],[rho2]])
        x0,y0=(0,0)
    
        if(abs(theta1-theta2)>1.3):
            x0, y0 = np.linalg.solve(A, b)
            x0, y0 = int(np.round(x0)), int(np.round(y0))
            
            return [[x0, y0]]
        

    def intersections_finder(lines):
        intersections = []
        for i, g in enumerate(lines[:-1]):
            for g2 in lines[i+1:]:
                for line1 in g:
                    for line2 in g2:
                        if(intersection(line1, line2)):
                            intersections.append(intersection(line1, line2)) 
        return intersections

    intersections = intersections_finder(j)
    i=np.asarray(intersections).reshape(len(intersections),2)
    best=[];
    bestmean=0;
    for item in list(combinations(i,4)):
        v=0;p=[]
        for it in item:
            if((it[0]<0 or it[1]<0) or (it[0]>imgt.shape[1] or it[1]>imgt.shape[0])):
                continue
            p.append(it);it=tuple(it)
        if(len(p)!=4):
            continue
        p=np.asarray(p)
        p = p.reshape(4,2)
        r= np.zeros((4,2), dtype="float32")
        s = np.sum(p, axis=1)
        r[0] = p[np.argmin(s)]
        r[2] = p[np.argmax(s)]
        d = np.diff(p, axis=1)
        r[1] = p[np.argmin(d)]
        r[3] = p[np.argmax(d)]
        (tl, tr, br, bl) =r
        if((tl[0]<tr[0])&(tr[1]<br[1])&(br[0]>bl[0])&(bl[1]>tl[1])):
            wA = np.sqrt((tl[0]-tr[0])**2 + (tl[1]-tr[1])**2 )
            wB = np.sqrt((bl[0]-br[0])**2 + (bl[1]-br[1])**2 )
            maxW = max(int(wA), int(wB))

            hA = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2 )
            hB = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2 )
            maxH = max(int(hA), int(hB))

            ds= np.array([[0,0],[maxW-1, 0],[maxW-1, maxH-1],[0, maxH-1]], dtype="float32")

            transformMatrix = cv.getPerspectiveTransform(r,ds)
            scan = cv.warpPerspective(gray, transformMatrix, (maxW, maxH))

            if(bestmean<scan.mean()):
                best=scan
                bestmean=scan.mean()

    ploter(best)
    return img


