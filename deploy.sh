if [ $# -ne 1]; then
  echo "指定された引数は$#個です。" 1>&2
  echo "実行するには3個の引数が必要です。" 1>&2
  exit 1
fi

git add -A
git commit -m $1
git push heroku main
heroku logs --tail