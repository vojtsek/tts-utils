cd /home/vojtech/marytts-5.2beta3/marytts-runtime/target/help_dir
rm -rf marytts
rm marytts-runtime-5.2-beta3-jar-with-dependencies.jar
cp -r ../classes/marytts/ .
jar cf marytts-runtime-5.2-beta3-jar-with-dependencies.jar *
cp marytts-runtime-5.2-beta3-jar-with-dependencies.jar /home/vojtech/marytts-5.2beta3/target/marytts-5.2-beta3/lib
