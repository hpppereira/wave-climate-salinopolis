% filtra vento

wd2 = zeros(1,248);
[b a]=butter(4,0.03);

y=wd1;
y=y*2*pi/360;
y=unwrap(y);
w1=y*360/(2*pi);
y1=cos(y);y2=sin(y);
w=zeros(1,248);
for i=5:248-5,
    g1=mean(y1(i-4:i+4));
    g2=mean(y2(i-4:i+4));
    g3=angle(g1+j*g2);g3=g3*360/(2*pi);
    if g3<0
        g3=g3+360;
    end;
    if g3>=360,
        g3=g3-360;
    end;
    w(i)=g3;
end;

g=find(w>360);
w(g)=w(g)-360;
g=find(w>360);
w(g)=w(g)-360;

g=find(w<0);
w(g)=w(g)+360;

wd2 = w