void main()
{
    int i, j, k, d, r, t, N;
    double score, _average, max=0.00, min=100.00, sum=0.00, O, P, Q;
    scanf(N);
    for (i=1; i<=N; i++)
    {
        scanf(score);
        if (max<score) max=score;
        if (min>score) min=score;
        sum=sum+score;
    }
    _average= (sum-max-min)/(N-2);
    j = 160; k= 40; d=j-k;
    O= 2.5E3; P= 4.6780; Q= O*P;
    r= j && k; t= j || k; @;
}

