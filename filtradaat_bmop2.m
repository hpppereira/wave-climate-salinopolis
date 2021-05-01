%**************************************************************************
% Programa filtrapledscearal.m para filtrar dados de direçao
%
% a) tira a media entre 2 pontos anteriores e 2 pontos posteriores;
% b) elimina direçoes cuja diferença seja maior que 60 graus.
%
%**************************************************************************

ddir=zeros(10,248);

for ik=1:10,
[b a]=butter(4,0.1);
y=dire1(ik,:)';
y=y*2*pi/360;
y=unwrap(y);
w1=y*360/(2*pi);
y1=cos(y);y2=sin(y);
w=zeros(1,248);
for i=3:246,
    g1=mean(y1(i-2:i+2));
    g2=mean(y2(i-2:i+2));
    g3=angle(g1+j*g2);g3=g3*360/(2*pi);
    if g3<0,g3=g3+360;end;
    if g3>=360,g3=g3-360;end;
    w(i)=g3;
end;

x=diff(w1);
x=abs(x);
g=find(x>60);
w(g+1)=NaN;

g=find(w>360);
w(g)=w(g)-360;
g=find(w>360);
w(g)=w(g)-360;

g=find(w<0);
w(g)=w(g)+360;
g=find(w<0);
w(g)=w(g)+360;
ddir(ik,:)=w;
end;

for i=1:248,
    for k=1:2:7,
        if energ(ceil(k/2),i)>0,
        espe(k:k+1,i)=espe(k:k+1,i)*energ(ceil(k/2),i)/sum(espe(k:k+1,i));
    end;end;
end









