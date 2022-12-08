#! /bin/bash
dir=~/Desktop/music/
FILES="${dir}*"
for f in $FILES.mp3
do
  # echo "${f%.*} :file..."
  re='([0-9]{2})\ (.+?)\ \((.+?)\)\.mp3'
  if [[ $f =~ $re ]]
  then
    track=${BASH_REMATCH[1]}
    title=${BASH_REMATCH[2]}
    artist=${BASH_REMATCH[3]}
    
        case $artist in
            "bush")
                artist="Tracy Bush"
                ;;
            "Bush")
                artist="Tracy Bush"
                ;;
            "Duke")
                artist="Derek Duke"
            ;;
            "Stafford")
                artist="Glenn Stafford"
                ;;
            "Hayes")
                artist="Jason Hayes"
                ;;
            *)
            ;;
        esac
        album="Warcraft 3 - Soundtrack"
        echo "$dir/front-cover.jpg"
        # id3tool -t "$title" -a "$album" -r "$artist" -y "2002" -c $track "$f"
        # --add-image "$dir/back-cover.jpg:BACK_COVER"
        eyeD3 -t "$title" -a "$artist" -A "$album" -n $track -Y 2002 --add-image "$dir/front-cover.jpg:FRONT_COVER" "$f"
        # eyeD3 --remove-all-images "$f"
        # Show info
        id3tool "$f"
    else
    echo "no match"
    fi

done
