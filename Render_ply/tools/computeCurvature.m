function C = computeCurvature(im, scale)

xmin = min(im(:,1));ymin = min(im(:,2));
xmax = max(im(:,1));ymax = max(im(:,2));

xscale = scale;yscale=scale;
[X1, Y1] = meshgrid(xmin:xscale:xmax,ymax:-yscale:ymin);%生成规则网格坐标X和Y,方向步长均取0.1

Z=griddata(im(:,1),im(:,2),im(:,3),X1,Y1); %#ok<*GRIDD>


% 有一定问题，和论文里使用的计算曲率图方法不一样
[K,H,P1,P2] = surfature(X1,Y1,Z);
ShapeIndex=0.5-(1/pi)*atan((P2+P1)./(P2-P1)); %计算形状指数参数

C_ = uint8(rescale(ShapeIndex, 0, 255));
[m, n] = size(C_);

C = zeros(m, n, 3);C(:,:,1) = C_;C(:,:,2) = C_;C(:,:,3) = C_;
C = uint8(C);


end