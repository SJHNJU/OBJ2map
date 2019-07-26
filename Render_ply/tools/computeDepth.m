function D = computeDepth(im, scale)

xmin = min(im(:,1));ymin = min(im(:,2));
xmax = max(im(:,1));ymax = max(im(:,2));

xscale = scale;yscale=scale;
[X1, Y1] = meshgrid(xmin:xscale:xmax,ymax:-yscale:ymin);%生成规则网格坐标X和Y,方向步长均取0.005

D_ = griddata(im(:,1),im(:,2),im(:,3),X1,Y1);
D_ = uint8(rescale(D_, 0, 255));
[m, n] = size(D_);

D = zeros(m, n, 3);D(:,:,1) = D_;D(:,:,2) = D_;D(:,:,3) = D_;
D = uint8(D);
end
