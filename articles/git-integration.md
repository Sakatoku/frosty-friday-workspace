# 快適！Frosty Friday生活！～Snowflake WorkspacesとGitHubを連携させよう

この記事は[Frosty Friday Advent Calendar 2025](https://qiita.com/advent-calendar/2025/frostyfriday)の1日目です。  
みんなでFrosty Fridayをやってみよう！  

## Frosy Fridayとは

Frosty Fridayとは「**Snowflakeユーザが、Snowflakeユーザのために作成し、Snowflakeスキルの練習と開発に役立つ**」チャレンジです。  
原文：  
*to help you practice and develop your Snowflake skills, created by Snowflake users, for Snowflake users.*  

[こちらのサイト](https://frostyfriday.org/)で毎週新しいチャレンジが公開されます。  
難易度はBasic/Easy(やさしい)、Intermediate(ほどほど)、Hard/Advanced(むずかしい)の3段階。やさしい問題はSnowflake初心者が勉強するために、ほどほど問題やむずかしい問題はSnowflake経験者が新しい機能を習得するためにちょうどいいものになっています！  

https://frostyfriday.org/

## Frosty Fridayの解答を投稿しよう！

単純にチャレンジを眺める、手元でやってみるだけでももちろん勉強になるのですが、ぜひ自分の解答をFrosty Fridayのサイトに投稿してみましょう！  
ちょっとしたことですが、投稿という形で実績が少しづつ積み上がっていくのはモチベーションを維持する助けになります！  
日本のSnowflakeユーザさんから「参考にしました！」という嬉しいお声がけをいただくこともたまにありますよー。  

解答投稿は以下のような手順で行います。  

1. 試行錯誤して解答を完成させる！
2. 完成した解答をGitHub[^1]にプッシュしておく
3. Frosty Fridayのサイトに[ユーザ登録(サインアップ)](https://frostyfriday.org/wp-signup.php)する
4. 解答を投稿したいチャレンジのページに移動
5. コメント欄の"Solution URL"にGitHubにプッシュした解答のURLを張る
6. コメント欄の"Comment"に好きなメッセージを書き込む。英語でも日本語でもいいと思うよ！

![投稿欄](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2917580/e8cb62ba-9d5e-4d9b-b6ad-47751d105358.png)

[^1]: パブリックなgitリポジトリならGitHub以外でもOK！

解答投稿のもっと詳細な手順は[こちらの記事](https://zenn.dev/churadata/articles/cb49f469dc9b56)が参考になります。  

注意事項として、一度投稿したURLやメッセージは修正できません…そこだけ気を付けましょう。  

## Snowflake WorkspacesとGitHubを連携させよう！

[Snowflake Workspaces](https://docs.snowflake.com/ja/user-guide/ui-snowsight/workspaces)とGitHubを連携させることで、作成したSQLファイルをSnowsight[^2]からポチポチでGitHubにプッシュすることができます。  
つまり、先述の流れのうち、2.を一動作(ワンアクション)減らすことができます！MASTERキートンもビックリだぜ。  

[^2]: SnowflakeのWebUI

SnowflakeにはSnowflake Workspacesがリリースされる前からgit連携のための機能があって、これを用いることでSnowflake WorkspacesとGitHubも連携させることができます。  
[Gitを使用するためのSnowflakeの設定](https://docs.snowflake.com/ja/developer-guide/git/git-setting-up)というドキュメントを参考にしましょう。  
色々な設定がありますが、手軽さだけなら  

- パブリックネットワーク経由でのアクセスで、
- OAuthフローで認証する。

のが一番じゃないかなと思います。ほぼ以下のコードを実行するだけ！  

```sql
CREATE OR REPLACE API INTEGRATION {任意のAPIインテグレーション名}
   API_PROVIDER = git_https_api
   API_ALLOWED_PREFIXES = ('https://github.com/')
   API_USER_AUTHENTICATION = (
      TYPE = snowflake_github_app
   )
   ENABLED = TRUE;
```

その後は[Integrate workspaces with a Git repository](https://docs.snowflake.com/en/user-guide/ui-snowsight/workspaces-git)というドキュメントに従ってワークスペースを作成しましょう！  

まず、ワークスペースを作成するためのメニューで"From Git repository"を選択して、  

![Create workspace from GitHub (1)](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2917580/46a85b6d-3c34-4e9e-8e50-07f914395f30.png)

ブランチがあるリポジトリ[^3]を指定すると、  

![Create workspace from GitHub (2)](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2917580/48ae5572-6a17-4cb5-9de2-efa5af450d52.png)

Authorizeを要求するよくある画面がポップアップするので許可したら、ワークスペースが作成されて使えるようになります。  

![GitHub authorize](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2917580/57a1852d-4a56-45c3-89a3-9ed0aace978d.png)

[^3]: 空のリポジトリからスタートしたい場合もREADME.mdなどを作成しておきましょう

作成したSQLファイルをプッシュするのは"Changes"ボタンから。  

![Using workspace with GitHub (1)](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2917580/d3879438-de18-4771-8e88-e3fcd120061d.png)

"Open repo page"からGitHubのリポジトリページにも飛べるので、プッシュしたSQLファイルのURLを取得するのも楽々ですね！  

![Using workspace with GitHub (2)](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/2917580/7f10721b-4da7-4178-bda1-977e1ab2bd12.png)

## まとめ

あらためて、皆さんもぜひ自分の解答をFrosty Fridayのサイトに投稿してみてくださいね！  
そして、こんなことをやったらチャレンジや投稿が快適になるよーみたいなライフハックも共有してくれると嬉しいです！  
