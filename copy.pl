#!/opt/nokia/oss/perl/bin/perl
use strict;
use Data::Dumper;
use Net::FTP;


my $dir_in = '/home/na_scripts/huawei/U2000/CURRENT/';
my $ftp = Net::FTP->new("10.XX.XX.101", debug => 1, Passive =>1) or die "Cannot connect to 10.XX.XX.101:  $@";
eval {
   $ftp->login("ftpXXX","anXXX") or die "Cannot login ", $ftp->message;
   printf "%s\n", $ftp->pwd();
   $ftp->cwd("/script") or die "Cannot change working directory ", $ftp->message;
   my @ls = $ftp->ls();
   my @dn;
   foreach my $dirn (@ls) {
     if ($dirn=~ /^Schedule_(.+)/) { 
	push @dn, $dirn;
	}
     }
   my $dir = $dn[$#dn];
   print "dir = $dir \n";
   $ftp->cwd("$dir") or die "Cannot change $dir directory ". $ftp->message;
   my @list = $ftp->ls() or die "ls failed ", $ftp->message;
   my ($fn,$lfn,$tof,$cc);
   foreach $fn (@list)  {
      $lfn = $fn;
      $lfn =~ s/_\(UTF-8\)//;
      $lfn =~ s/\s+/_/gm;
      print " $fn  \n"; 
      my ($v1,$d1,$t1) = split /_/, $dir;  
       if ($fn=~ /^NWC(.+)/) {
         $tof = "$dir_in$lfn"."_$d1";
         $ftp->get("$fn","$tof") or die "get $fn failed ", $ftp->message;
         $cc++;  
        print "$cc: $fn ---> $tof  \n";
        }  
       elsif ($fn=~ /^NED(.+)/) {
         $tof = "$dir_in$lfn";
         $ftp->get("$fn","$tof") or die "get $fn failed ", $ftp->message;
         $cc++;
         print "$cc: $fn ---> $tof  \n";
         }
=comment  
       elsif ($fn=~ /^Micro(.+)/) {
         my $lnkf =  $fn;
         $lnkf =~ s/\s+/_/gm; 
         $lnkf=~ s/\(csv\)/txt/;
         $tof = "$dir_in$lnkf";
         print "$fn==> $tof\n";  
         $ftp->get("$fn","$tof") or die "get $fn failed ", $ftp->message;
         }
=cut
      } #foreach
    $ftp->cwd("/script") or die "Cannot change working directory ", $ftp->message;
    @ls = $ftp->ls();
    print  Data::Dumper->Dumpxs([\@ls ],[qw(*skript_RTN)]) ;
       foreach $fn (@list)  {
            $lfn = $fn;
            $lfn =~ s/\s+/_/gm;
            $tof = "$dir_in$lfn";
            print " $fn ---> $tof  \n";
            
      } #foreach
    $ftp->cwd("/link_report") or die "Cannot change working directory ", $ftp->message;
    @ls = $ftp->ls();
    print  Data::Dumper->Dumpxs([\@ls ],[qw(*ls)]) ;
    my $end = $#ls;
    print "link_report $end -> $ls[$end]";
     $fn=$ls[$end];
     my $lnkf = $fn;
     $lnkf =~ s/\s+/_/gm;
     $lnkf=~ s/\(csv\)/txt/;
     my $lnk = "Microwave_Link_Report.txt";
     $tof = "$dir_in$lnk";
     $ftp->get("$fn","$tof") or die "get $fn failed ", $ftp->message;
   $ftp->quit;
}; #of  eval
if ($@) {
      my $msg = $@;
      print "err = $msg\n";
      }


