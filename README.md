# Brazilian Portuguese Grammar（ブラジルポルトガル語 文法書）

日常会話を目標にした、ブラジルポルトガル語の文法書です。1項目5分で読めるレッスンを少しずつ増やしていきます。
GitHub Pages で公開し、PC・スマホのブラウザから読めます。

- 本文は英語、執筆ルールは `CLAUDE.md`
- 全体の章立て（完成予定図）は `_data/toc.yml`
- レッスン本体は `lessons/`

## ファイル構成

```
_config.yml          サイト設定（タイトル、公開URLのパス）
_data/toc.yml        全体の章立て。各項目の status を published にすると目次にリンクが付く
_layouts/            ページの共通デザイン（出典欄・前後リンクは自動で付く）
assets/style.css     見た目（スマホ対応・ダークモード対応）
index.html           目次ページ
about.md             この本について・確認状況ラベルの説明
lessons/             レッスン（1項目＝1ファイル）
CLAUDE.md            執筆ルール（サイトには表示されない）
```

---

## GitHub Pages で公開する手順（初回のみ）

GitHub のアカウントがある前提です。所要時間は10分ほどです。

### 1. GitHub にリポジトリを作る

1. ブラウザで <https://github.com/new> を開く
2. **Repository name** に `portuguese-grammar` と入力
   （別の名前にする場合は、`_config.yml` の `baseurl` も `"/別の名前"` に変える）
3. **Public** を選ぶ（無料プランで GitHub Pages を使うには Public が必要）
4. 「Add a README file」などのチェックは **すべて外したまま**
5. **Create repository** を押す

### 2. 手元のファイルを GitHub に送る

ターミナルで次を1行ずつ実行します（`<ユーザー名>` は自分の GitHub ユーザー名に置き換え）。

```sh
cd ~/Developer/personal/portuguese-grammar
git init
git add .
git commit -m "First lesson: subject pronouns"
git branch -M main
git remote add origin https://github.com/<ユーザー名>/portuguese-grammar.git
git push -u origin main
```

> `gh` コマンドを使う場合は、上の `git remote add` と `git push` の代わりに
> `gh repo create portuguese-grammar --public --source=. --push` 1行でも同じことができます（手順1も不要）。

### 3. GitHub Pages を有効にする

1. GitHub のリポジトリページで **Settings**（歯車）を開く
2. 左メニューの **Pages** を開く
3. **Build and deployment** の **Source** で「**Deploy from a branch**」を選ぶ
4. **Branch** で `main`、フォルダは `/ (root)` を選び、**Save**
5. 1〜3分待つと、同じ画面の上部に公開URLが表示される
   - URL は `https://<ユーザー名>.github.io/portuguese-grammar/`
   - リポジトリの **Actions** タブで進捗（緑のチェックで完了）を確認できる

### 4. スマホで読みやすくする

公開URLをスマホのブラウザで開き、
- iPhone（Safari）：共有ボタン →「ホーム画面に追加」
- Android（Chrome）：メニュー →「ホーム画面に追加」

でアプリのように開けます。

---

## 2回目以降：レッスンを追加したとき

Claude にレッスンを書いてもらったあと、次の3行で公開されます（数分で反映）。

```sh
cd ~/Developer/personal/portuguese-grammar
git add .
git commit -m "Add lesson 01-02"
git push
```

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| ページは出るがデザインが崩れている | `_config.yml` の `baseurl` がリポジトリ名と一致しているか |
| 404 が出る | Settings → Pages で Branch が `main` / `/ (root)` になっているか。数分待ったか |
| 更新が反映されない | Actions タブでビルドが失敗（赤い×）していないか。失敗していたらエラー内容を Claude に見せる |
