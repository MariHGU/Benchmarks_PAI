public static int SumArray(int[] arr) {
    int sum = 0;
    foreach (int num in arr) {
        sum += num;
    }
    return sum;
}