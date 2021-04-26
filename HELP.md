# Tools & Tests

## Unit test

Unit test are run inside the lts qgis image gis/qgis:release-3_16

```bash
docker run --rm -it --name qgis -v /tmp/.X11-unix:/tmp/.X11-unix  -e DISPLAY=unix$DISPLAY qgis/qgis:release-3_16
docker run -d --name qgis_test -v /tmp/.X11-unix:/tmp/.X11-unix  -v /your/path/to/q3m/:/home/q3m  -e DISPLAY=:99  qgis/qgis:release-3_16
```

```bash
docker exec -it qgis_test bash
cd /home/q3m

python -m unittest discover
coverage report -m test/test_*
```

## Translations
- Add new files i18n/qm3.pro and then run the two following lines

| Make sure you have the qt tools installed before running the following commands

```bash
# generate ts files and qm files
cd i18n
pylupdate5 q3m.pro
lrelease-qt5 MapMatching_en.ts MapMatching_fr.ts
```


