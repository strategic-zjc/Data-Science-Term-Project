public class WildcardMatching {
    public boolean isMatch(String s, String p) {
        int m = s.length(), n = p.length();
        boolean[][] dp = new boolean[m+1][n+1];
        dp[0][0] = true;
        for(int j = 1; j <= n; j++) dp[0][j]= (p.charAt(j-1)=='*') ? dp[0][j-1] : dp[0][j];
        for(int i = 1; i <= m; i++) {
            for(int j = 1; j <= n; j++) {
                if(p.charAt(j-1) == '*') dp[i][j] = (dp[i-1][j] || dp[i][j-1]);
                else dp[i][j] = (s.charAt(i-1) == p.charAt(j-1) || p.charAt(j-1) == '?') && dp[i-1][j-1];
            }
        }
        return dp[m][n];
    }
}