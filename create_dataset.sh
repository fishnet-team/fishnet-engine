wget -O gm2017.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2017_standard2000_nomovetimes_67471.pgn.bz2
wget -O gm2016.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2016_standard2000_nomovetimes_67475.pgn.bz2
wget -O gm2015.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2015_standard2000_nomovetimes_67476.pgn.bz2
wget -O gm2014.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2014_standard2000_nomovetimes_67477.pgn.bz2
wget -O gm2013.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2013_standard2000_nomovetimes_67478.pgn.bz2
wget -O gm2012.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2012_standard2000_nomovetimes_67479.pgn.bz2
wget -O gm2011.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2011_standard2000_nomovetimes_67480.pgn.bz2
wget -O gm2010.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2010_standard2000_nomovetimes_67481.pgn.bz2
wget -O gm2009.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2009_standard2000_nomovetimes_67482.pgn.bz2
wget -O gm2008.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2008_standard2000_nomovetimes_67483.pgn.bz2
wget -O gm2007.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2007_standard2000_nomovetimes_67484.pgn.bz2
wget -O gm2006.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2006_standard2000_nomovetimes_67485.pgn.bz2
wget -O gm2005.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2005_standard2000_nomovetimes_67486.pgn.bz2
wget -O gm2004.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2004_standard2000_nomovetimes_67487.pgn.bz2
wget -O gm2003.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2003_standard2000_nomovetimes_67488.pgn.bz2
wget -O gm2002.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2002_standard2000_nomovetimes_67490.pgn.bz2
wget -O gm2001.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2001_standard2000_nomovetimes_67491.pgn.bz2
wget -O gm2000.pgn.bz2 https://www.ficsgames.org/dl/ficsgamesdb_2000_standard2000_nomovetimes_67492.pgn.bz2

rm fics_gm.pgn
bzip2 -d gm*.pgn.bz2

cat gm*.pgn >> fics_gm.pgn

