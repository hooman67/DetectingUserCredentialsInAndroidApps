pass = strcmp(hints, passWords(1,1));
for i=2:size(passWords,1)
    pass = pass + strcmp(hints, passWords(i,1));
end

user = strcmp(hints, userWords(1,1));
for i=2:size(userWords,1)
    user = user + strcmp(hints, userWords(i,1));
end
user = user * 2;

pred = user + pass;

Er = mean(double(pred == labels))*100

