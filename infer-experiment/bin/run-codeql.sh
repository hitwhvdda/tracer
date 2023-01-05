PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
BENCH_LIST=$PROJECT_HOME/result/selected-packages.txt
CODEQL_HOME=$PROJECT_HOME/codeql/codeql-home
BIN_DIR=$PROJECT_HOME/codeql/codeql-bin

DOCKER_IMAGE=prosyslab/bug-bench-base

declare -a bench_list=($(cat $BENCH_LIST))

for bench in "${bench_list[@]}"; do
    beginTime=$(date +%s%N)
    echo $bench
    CONTAINER_IMAGE=$(docker run --rm -i -v $CODEQL_HOME/:/codeql-home -v $BIN_DIR/:/bin_dir --detach $DOCKER_IMAGE /bin/bash)
    echo -n > $BIN_DIR/logs/$bench-database-log.txt
    docker exec -i $CONTAINER_IMAGE bash -c "cd /src && \
                                            apt update > /bin_dir/logs/$bench-database-log.txt && \
                                            apt source $bench > /bin_dir/logs/$bench-database-log.txt && \
                                            export PATH=$PATH:/codeql-home/codeql && \
                                            rm -rf /codeql-home/db-$bench && \
                                            rm -rf compile_commands.json && \
                                            chmod 777 /bin_dir/create-database.sh && \
                                            /bin_dir/create-database.sh $bench >> /bin_dir/logs/$bench-database-log.txt && \
                                            echo create $bench >> /bin_dir/finished_bench.txt
                                            cd /codeql-home && \
                                            chmod 777 /bin_dir/analyze-database.sh && \
                                            /bin_dir/analyze-database.sh $bench"
    endTime=$(date +%s%N) 
    elapsed=`echo "($endTime - $beginTime) / 1000000" | bc` 
    elapsedSec=`echo "scale=6;$elapsed / 1000" | bc | awk '{printf "%.6f", $1}'` 
    echo $bench: $elapsedSec sec >> $BIN_DIR/logs/time.txt
done