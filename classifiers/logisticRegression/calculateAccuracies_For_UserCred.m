function [ Er ] = lrHsEr( y, X, all_theta )

pred = predictOneVsAll(all_theta, X);

Er = mean(double(pred == y))*100;

tp = sum( (y>1) & (pred>1) );

fp = sum( (y==1) & (pred>1) );

fn = sum( (y>1) &  (pred==1));

prec = tp/(tp+fp);
rec = tp/(tp+fn);


fprintf('\nAccuracy: %f\n', mean(double(pred == y)) * 100);
fprintf('\nPrecision: %f\n', prec * 100);
fprintf('\nRecall: %f\n', rec * 100);

end

