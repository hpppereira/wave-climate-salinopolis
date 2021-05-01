% filtra a a serie de direcao da daat

% entra com os a matriz de direcao (amostragem de 1 ou 3 h)
[l, c] = size(ddir);

% monta filtro
[b a] = butter(3,0.1);

% cria matriz de saida do mesmo tamanho
% da matriz de entrada
ddir = zeros(l, c);

% loop das linhas (2 direcoes por faixa = 8 linhas)
for ik = 1:l
    
    % serie de direcao
    h = ddir(ik,:);
    hh = h;
    
    % acha valores de direcao maior que zero
    g = find(h > 0);
    % derivada da serie de direcao
    g1 = diff(g);
    % acha derivadas positivas
    g2 = find(g1 > 1);
    % cria matriz com 2 colunas e quantidade de
    % derivadas positivas da direcao
    k = zeros(2,length(g2)-1);

    % loop das derivadas positivas
    for i = 1:length(g2)
        k(1,i) = g(g2(i));
        k(2,i) = g(g2(i)) + g1(g2(i));
    end

    % faz uma interpolacao
    g8 = diff(k);
    if length(g8) > 1
        for i=1:length(k),
            if g8(i)<4,
                y = [h(k(1,i)); h(k(2,i))];
                x = [k(1,i); k(2,i)];
                xi = (k(1,i):k(2,i))';
                yi = interp1(x, y, xi);
                hh(xi') = yi';
            end
        end
    end

    % converte para radianos?
    hh = hh * 2 * pi / 360;

    s1 = [];
    s2 = [];
    g3 = [];

    % loop de cada valor de direcao
    for i = 1:c
        if hh(i) > 0
            s1 = [s1; hh(i)];
            s2 = [s2;i];                     
        else
            if length(s1) > 9,
                z1 = cos(s1);
                z1 = filtfilt(b, a, z1);
                z2 = sin(s1);
                z2 = filtfilt(b, a, z2);
                g3 = angle(z1 + j*z2);
                % transforma de rad para graus
                g3 = g3 * 360 / (2*pi);
                             
                % corrige valores menores que 0 e maiores que 360
                g4 = find(g3<0);
                g3(g4) = g3(g4) + 360;
                g4 = find(g3>=360);
                g3(g4) = g3(g4)-360;

                ddir(ik,s2(1):s2(end)) = g3;
                
                s1 = [];
                s2 = [];
                g3 = [];
            else
                if length(s1) > 0
                    ddir(ik,s2(1):s2(end)) = s1 * 180/pi;
                    s1 = [];
                    s2 = [];
                    g3 = [];
                end
            end
        end
    end
end