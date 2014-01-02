#!/usr/bin/env perl

use Image::EXIF;
use Data::Dumper;
use File::stat;
use POSIX qw(strftime);


sub read_exif_and_rename
{
	my $exif = shift;
	my $file_name = shift;
	my $extension = shift;

	if ($extension eq "bmp" or $extension eq "BMP") {
		my $st = stat($file_name);
		$new_name = strftime("%Y_%m_%d %H_%M_%S", localtime($st->mtime)) . "." . $extension;
	} else {
		$exif->file_name($file_name);
		my $image_info = $exif->get_image_info();
		$created_time = $image_info->{"Image Created"};
		if (-e $new_name) {
			$new_name = $created_time . "-1." . $extension;
		} else {
			$new_name = $created_time . "." . $extension;
		}
	}
	print "$file_name --> $new_name\n";
	rename($file_name, $new_name);
}


sub main
{
	my $file_name = $ARGV[0];
	$file_name =~ m!(jpg|png|bmp|gif)!i;
	my $extension = $1;
	my $exif = Image::EXIF->new;
	read_exif_and_rename($exif, $file_name, $extension);
}


main();
